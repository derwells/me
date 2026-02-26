from datetime import date

import pytest
from pydantic import ValidationError

from ralph.config import Loop, LoopStatus, LoopType


def test_valid_loop():
    loop = Loop(
        description="Test loop",
        type=LoopType.REVERSE,
        status=LoopStatus.ACTIVE,
        max_iterations=30,
        timeout_seconds=900,
        model="claude-opus-4-6",
        created=date(2026, 2, 25),
    )
    assert loop.description == "Test loop"
    assert loop.type == LoopType.REVERSE
    assert loop.status == LoopStatus.ACTIVE
    assert loop.max_iterations == 30
    assert loop.timeout_seconds == 900
    assert loop.converged_at is None


def test_loop_defaults():
    loop = Loop(
        description="Test loop",
        type=LoopType.REVERSE,
        status=LoopStatus.ACTIVE,
        max_iterations=30,
        timeout_seconds=900,
        created=date(2026, 2, 25),
    )
    assert loop.model == "claude-opus-4-6"
    assert loop.converged_at is None


def test_loop_rejects_zero_iterations():
    with pytest.raises(ValidationError):
        Loop(
            description="Test loop",
            type=LoopType.REVERSE,
            status=LoopStatus.ACTIVE,
            max_iterations=0,
            timeout_seconds=900,
            created=date(2026, 2, 25),
        )


def test_loop_rejects_negative_timeout():
    with pytest.raises(ValidationError):
        Loop(
            description="Test loop",
            type=LoopType.REVERSE,
            status=LoopStatus.ACTIVE,
            max_iterations=30,
            timeout_seconds=-1,
            created=date(2026, 2, 25),
        )


def test_invalid_status_string():
    with pytest.raises(ValidationError):
        Loop(
            description="Test loop",
            type=LoopType.REVERSE,
            status="running",
            max_iterations=30,
            timeout_seconds=900,
            created=date(2026, 2, 25),
        )


def test_invalid_type_string():
    with pytest.raises(ValidationError):
        Loop(
            description="Test loop",
            type="sideways",
            status=LoopStatus.ACTIVE,
            max_iterations=30,
            timeout_seconds=900,
            created=date(2026, 2, 25),
        )
