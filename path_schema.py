"""Pydantic models for robot path plans extracted from grid sketches."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator


class Command(BaseModel):
    type: Literal["straight", "turn"]
    distance: int | None = None
    angle: int | None = None

    @model_validator(mode="after")
    def validate_command(self) -> Command:
        if self.type == "straight":
            if self.distance is None or self.distance <= 0:
                raise ValueError("straight commands require distance > 0")
        else:
            if self.angle is None or self.angle == 0:
                raise ValueError("turn commands require a non-zero angle")
            if self.angle < -360 or self.angle > 360:
                raise ValueError("turn angle must be between -360 and 360")
        return self


class PathPlan(BaseModel):
    commands: list[Command] = Field(min_length=1)
