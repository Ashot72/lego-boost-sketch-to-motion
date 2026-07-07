"""OpenAI vision extraction for grid-path sketches."""

from __future__ import annotations

import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from path_schema import PathPlan

load_dotenv()

MODEL = "gpt-5.5"
PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "path_extraction.txt"


def _load_system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def _encode_image(image_path: Path) -> str:
    return base64.standard_b64encode(image_path.read_bytes()).decode("ascii")


def parse_path_image(image_path: str | Path) -> PathPlan:
    """Analyze a grid-path screenshot and return a validated PathPlan."""
    path = Path(image_path)
    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")

    api_key = os.getenv("OPENAI_API_KEY")
    image_data = _encode_image(path)
    client = OpenAI(api_key=api_key)

    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": _load_system_prompt()},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract the path plan from this sketch.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_data}",
                        },
                    },
                ],
            },
        ],
        response_format=PathPlan,
    )

    message = completion.choices[0].message
    if message.parsed is None:
        raise RuntimeError("OpenAI did not return a structured path plan")

    return message.parsed
