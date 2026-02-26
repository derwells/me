import typer

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """Ralph — typed loop runner."""


@app.command()
def status() -> None:
    """Print registry status table."""
    typer.echo("ralph CLI is working")


if __name__ == "__main__":
    app()
