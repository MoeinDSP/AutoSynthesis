"""Utility helpers for logging, I/O, and formatting."""

import os
import json
import logging
from typing import Any


def setup_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=level,
    )


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def save_json(data: Any, path: str) -> None:
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def fmt(value: float, decimals: int = 4) -> str:
    """Format a float to a fixed number of decimal places."""
    return f"{value:.{decimals}f}"


def significance_stars(p: float) -> str:
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return ""
