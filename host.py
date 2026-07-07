"""
PC host for LegoBoostVision — grid sketch to DriveBase path via OpenAI vision.

Usage:
  host.bat

Put your sketch at input/sketch.png before running.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

from host_path import (
    prepare_path_drive_run,
    resolve_input_image,
    save_path_plan,
)
from host_ai import parse_path_image

GENERATED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_generated")

HUB_TIPS = """
Hub not found. Check: hub ON, Pybricks firmware, Boost app closed, Bluetooth on.
Try: host.bat -n "Pybricks Hub" --timeout 60
"""


def _process_image(image_path: Path) -> str:
    print(f"Analyzing: {image_path}", flush=True)
    plan = parse_path_image(image_path)
    json_path = save_path_plan(plan, image_path.stem)
    print(f"Saved JSON: {json_path}", flush=True)
    print(json.dumps(plan.model_dump(), indent=2), flush=True)

    script_path = prepare_path_drive_run(GENERATED_DIR, plan)
    print(f"Generated: {script_path}", flush=True)
    return script_path


async def _deploy_path(hub, script_path: str) -> None:
    await hub.stop_user_program()
    print(f"Uploading: {script_path}", flush=True)
    await hub.run(script_path, wait=False, print_output=False, line_handler=False)
    print("Deployed. Run host.bat again for the next sketch.", flush=True)


async def _run_host(image_path: Path, hub_name: str | None, timeout: float) -> int:
    from pybricksdev.ble import find_device
    from pybricksdev.connections.pybricks import PybricksHubBLE

    try:
        script_path = _process_image(image_path)
    except Exception as exc:
        print(f"failed: {exc}", flush=True)
        return 1

    print(f"Searching for hub ({timeout:.0f} s)...")
    try:
        device = await find_device(hub_name, timeout=timeout)
    except asyncio.TimeoutError:
        print(HUB_TIPS)
        return 1

    hub = PybricksHubBLE(device)
    await hub.connect()
    print("Connected.", flush=True)

    try:
        await _deploy_path(hub, script_path)
        return 0
    except Exception as exc:
        print(f"Deploy failed: {exc}", flush=True)
        return 1
    finally:
        await hub.disconnect()


def main() -> int:
    parser = argparse.ArgumentParser(description="LegoBoost OpenAI mission host")
    parser.add_argument("-n", "--name", help="Bluetooth hub name")
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    try:
        image_path = resolve_input_image()
    except FileNotFoundError as exc:
        print(exc, flush=True)
        return 1

    return asyncio.run(_run_host(image_path, args.name, args.timeout))


if __name__ == "__main__":
    sys.exit(main())
