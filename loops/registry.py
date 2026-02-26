"""
Ralph Loop Registry — typed, validated at import time.

Add new loops here. Invalid entries cause immediate ImportError with a clear message.
"""

from datetime import date

from ralph.config import Loop, LoopStatus, LoopType

LOOPS: dict[str, Loop] = {
    "reverse-github-profile": Loop(
        description="Audit GitHub profile → profile spec",
        type=LoopType.REVERSE,
        status=LoopStatus.ACTIVE,
        max_iterations=25,
        timeout_seconds=600,
        created=date(2026, 2, 24),
    ),
    "reverse-linkedin-profile": Loop(
        description="Mine repos + work projects → full LinkedIn profile spec",
        type=LoopType.REVERSE,
        status=LoopStatus.CONVERGED,
        max_iterations=25,
        timeout_seconds=900,
        created=date(2026, 2, 24),
        converged_at=date(2026, 2, 24),
    ),
    "reverse-ph-tax-computations": Loop(
        description="Survey PH real estate tax computations → ranked automation opportunity catalog",
        type=LoopType.REVERSE,
        status=LoopStatus.ACTIVE,
        max_iterations=30,
        timeout_seconds=900,
        model="claude-opus-4-6",
        created=date(2026, 2, 25),
    ),
    "reverse-ph-land-title-coordinates": Loop(
        description="PH land title technical description → WGS84 lat/lng computation engine spec",
        type=LoopType.REVERSE,
        status=LoopStatus.ACTIVE,
        max_iterations=20,
        timeout_seconds=900,
        created=date(2026, 2, 26),
    ),
    "reverse-ph-realestate-calcs": Loop(
        description="Survey PH non-tax real estate calculations → ranked automation opportunity catalog",
        type=LoopType.REVERSE,
        status=LoopStatus.ACTIVE,
        max_iterations=40,
        timeout_seconds=900,
        created=date(2026, 2, 26),
    ),
    "reverse-tsvj-backoffice-automation": Loop(
        description="Survey back-office tasks for Las Piñas SEC-registered rental property business → process catalog with feature specs",
        type=LoopType.REVERSE,
        status=LoopStatus.ACTIVE,
        max_iterations=40,
        timeout_seconds=900,
        created=date(2026, 2, 26),
    ),
}
