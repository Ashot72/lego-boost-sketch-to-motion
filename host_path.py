"""Stage path scripts for hub upload."""

from __future__ import annotations

import json
import re
from pathlib import Path

from path_schema import Command, PathPlan
from template import path_drive

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
INPUT_DIR = ROOT / "input"
SKETCH_PATH = INPUT_DIR / "sketch.png"

_PATH_TEMPLATE = Path(path_drive.__file__)
_HOST_COMMANDS_RE = re.compile(
    r"    # --- HOST_COMMANDS_START ---\r?\n.*?    # --- HOST_COMMANDS_END ---\r?\n",
    re.DOTALL,
)


def load_path_plan(stem: str) -> PathPlan:
    path = OUTPUT_DIR / f"{stem}.json"
    if not path.is_file():
        raise FileNotFoundError(f"Path plan not found: {path}")
    return PathPlan.model_validate_json(path.read_text(encoding="utf-8"))


def resolve_input_image() -> Path:
    if not SKETCH_PATH.is_file():
        raise FileNotFoundError(f"Sketch not found: {SKETCH_PATH}")
    return SKETCH_PATH


def _command_to_line(command: Command) -> str:
    if command.type == "straight":
        return f"robot.straight({command.distance})"
    return f"robot.turn({command.angle})"


def _commands_block(plan: PathPlan, indent: str = "    ") -> str:
    lines = [f"{indent}{_command_to_line(command)}" for command in plan.commands]
    return "\n".join(lines) + "\n"


def save_path_plan(plan: PathPlan, stem: str) -> Path:
    dst = OUTPUT_DIR / f"{stem}.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(
        json.dumps(plan.model_dump(), indent=2) + "\n",
        encoding="utf-8",
    )
    return dst


def prepare_path_drive_run(generated_dir: str, plan: PathPlan) -> str:
    """Inject path commands into the template and write to _generated/."""
    dst = Path(generated_dir) / _PATH_TEMPLATE.name
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = _PATH_TEMPLATE.read_text(encoding="utf-8")

    block = _commands_block(plan)
    if not _HOST_COMMANDS_RE.search(text):
        raise ValueError(f"{_PATH_TEMPLATE} is missing HOST_COMMANDS block")

    text = _HOST_COMMANDS_RE.sub(
        "    # --- HOST_COMMANDS_START ---\n"
        + block
        + "    # --- HOST_COMMANDS_END ---\n",
        text,
        count=1,
    )

    dst.write_text(text, encoding="utf-8")
    return str(dst)
