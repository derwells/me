from datetime import date
from enum import Enum

from pydantic import BaseModel, field_validator


class LoopType(str, Enum):
    REVERSE = "reverse"
    FORWARD = "forward"


class LoopStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CONVERGED = "converged"


class Loop(BaseModel):
    description: str
    type: LoopType
    status: LoopStatus
    max_iterations: int
    timeout_seconds: int
    model: str = "claude-opus-4-6"
    created: date
    converged_at: date | None = None

    @field_validator("max_iterations")
    @classmethod
    def positive_iterations(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("max_iterations must be positive")
        return v

    @field_validator("timeout_seconds")
    @classmethod
    def positive_timeout(cls, v: int) -> int:
        if v < 0:
            raise ValueError("timeout_seconds must be non-negative")
        return v
