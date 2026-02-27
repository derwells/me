import os
import time
from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer

from ralph.config import Loop, LoopStatus, LoopType
from ralph.discover import discover_active_loops, format_github_matrix
from ralph.preflight import CheckSeverity, has_errors, run_preflight
from ralph.runner import run_iteration
from ralph.settings import RalphSettings

app = typer.Typer(no_args_is_help=True)

# Resolve loops/ directory relative to this repo
REPO_ROOT = Path(__file__).resolve().parents[2]
LOOPS_DIR = REPO_ROOT / "loops"


def _load_registry() -> dict[str, Loop]:
    """Import the registry module from loops/registry.py."""
    import importlib
    import importlib.util

    spec = importlib.util.spec_from_file_location("registry", LOOPS_DIR / "registry.py")
    if spec is None or spec.loader is None:
        typer.secho("Error: could not load loops/registry.py", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    loops: dict[str, Loop] = module.LOOPS  # type: ignore[attr-defined]
    return loops


def _load_settings() -> RalphSettings:
    """Load and validate settings from environment."""
    try:
        return RalphSettings()  # pyright: ignore[reportCallIssue]
    except Exception as e:
        typer.secho(f"Configuration error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from None


class OutputFormat(StrEnum):
    TABLE = "table"
    GITHUB_MATRIX = "github-matrix"


_STATUS_COLORS: dict[LoopStatus, str] = {
    LoopStatus.ACTIVE: typer.colors.GREEN,
    LoopStatus.PAUSED: typer.colors.YELLOW,
    LoopStatus.CONVERGED: typer.colors.CYAN,
}

_SEVERITY_COLORS: dict[CheckSeverity, str] = {
    CheckSeverity.OK: typer.colors.GREEN,
    CheckSeverity.WARNING: typer.colors.YELLOW,
    CheckSeverity.ERROR: typer.colors.RED,
}

_SEVERITY_ICONS: dict[CheckSeverity, str] = {
    CheckSeverity.OK: "\u2713",
    CheckSeverity.WARNING: "\u26a0",
    CheckSeverity.ERROR: "\u2717",
}


@app.command()
def status() -> None:
    """Print registry status table."""
    loops = _load_registry()
    typer.echo(f"{'Name':<45} {'Type':<10} {'Status':<12} {'Max Iter':<10}")
    typer.echo("-" * 77)
    for name, loop in loops.items():
        color = _STATUS_COLORS.get(loop.status, typer.colors.WHITE)
        status_str = typer.style(loop.status.value, fg=color)
        typer.echo(f"{name:<45} {loop.type.value:<10} {status_str:<21} {loop.max_iterations:<10}")


@app.command()
def discover(
    output: Annotated[OutputFormat, typer.Option(help="Output format")] = OutputFormat.TABLE,
    loop_type: Annotated[str | None, typer.Option("--type", help="Filter by loop type")] = None,
) -> None:
    """Discover active loops. Use --output github-matrix for CI."""
    loops = _load_registry()
    type_filter = LoopType(loop_type) if loop_type else None
    active = discover_active_loops(loops, LOOPS_DIR, loop_type=type_filter)

    if output == OutputFormat.GITHUB_MATRIX:
        matrix_json = format_github_matrix(active)
        typer.echo(matrix_json)
        # Set GitHub Actions outputs if running in CI
        github_output = os.environ.get("GITHUB_OUTPUT")
        if github_output:
            with open(github_output, "a") as f:
                f.write(f"matrix={matrix_json}\n")
                f.write(f"has_loops={'true' if active else 'false'}\n")
    else:
        if not active:
            typer.echo("No active loops found.")
        else:
            typer.echo(f"Active loops ({len(active)}):")
            for name in active:
                typer.echo(f"  - {name}")


@app.command()
def preflight(
    loop_name: Annotated[str, typer.Argument(help="Loop name from registry")],
) -> None:
    """Run preflight checks for a loop."""
    loops = _load_registry()
    if loop_name not in loops:
        typer.secho(f"Error: loop '{loop_name}' not in registry", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    loop_config = loops[loop_name]
    loop_dir = LOOPS_DIR / loop_name

    results = run_preflight(loop_name, loop_dir, loop_config)

    for r in results:
        icon = _SEVERITY_ICONS[r.severity]
        color = _SEVERITY_COLORS[r.severity]
        typer.secho(f"  {icon} {r.message}", fg=color, err=True)

    if has_errors(results):
        typer.secho("\nPreflight failed.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    else:
        typer.secho("\nPreflight passed.", fg=typer.colors.GREEN, err=True)


@app.command()
def run(
    loop_name: Annotated[str, typer.Argument(help="Loop name from registry")],
    iterations: Annotated[int, typer.Option("-n", "--iterations", help="Max iterations to run")] = 1,
    sleep_between: Annotated[int, typer.Option("--sleep", help="Seconds between iterations")] = 5,
) -> None:
    """Run loop iterations. Includes preflight check."""
    loops = _load_registry()
    settings = _load_settings()

    if loop_name not in loops:
        typer.secho(f"Error: loop '{loop_name}' not in registry", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    loop_config = loops[loop_name]
    loop_dir = LOOPS_DIR / loop_name

    # Preflight
    typer.secho(f"=== Preflight: {loop_name} ===", bold=True, err=True)
    results = run_preflight(loop_name, loop_dir, loop_config)
    for r in results:
        icon = _SEVERITY_ICONS[r.severity]
        color = _SEVERITY_COLORS[r.severity]
        typer.secho(f"  {icon} {r.message}", fg=color, err=True)

    if has_errors(results):
        typer.secho("\nPreflight failed. Aborting.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    # Run iterations
    consecutive_failures = 0
    converged_file = loop_dir / "status" / "converged.txt"

    for i in range(1, iterations + 1):
        if converged_file.exists():
            typer.secho("\nLoop converged!", fg=typer.colors.CYAN, err=True)
            break

        typer.secho(f"\n--- Iteration {i}/{iterations} ---", bold=True, err=True)
        result = run_iteration(loop_name, loop_dir, settings, loop_config)

        if result.success:
            typer.secho(f"Iteration {i} succeeded.", fg=typer.colors.GREEN, err=True)
            consecutive_failures = 0
        else:
            typer.secho(f"Iteration {i} failed: {result.error}", fg=typer.colors.RED, err=True)
            consecutive_failures += 1
            if consecutive_failures >= 3:
                typer.secho("3 consecutive failures. Stopping.", fg=typer.colors.RED, err=True)
                raise typer.Exit(code=1)

        if i < iterations and not converged_file.exists():
            time.sleep(sleep_between)

    # Final status
    if converged_file.exists():
        typer.secho(f"\n=== {loop_name}: CONVERGED ===", fg=typer.colors.CYAN, bold=True, err=True)
    else:
        typer.secho(f"\n=== {loop_name}: completed {iterations} iteration(s) ===", bold=True, err=True)


if __name__ == "__main__":
    app()
