from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


DATA_EXTENSIONS = {".json", ".yaml", ".yml"}


def load_data(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    text = source.read_text(encoding="utf-8")
    if source.suffix.lower() == ".json":
        data = json.loads(text)
    elif source.suffix.lower() in {".yaml", ".yml"}:
        data = yaml.safe_load(text)
    else:
        raise ValueError(f"Unsupported data file extension: {source.suffix}")

    if not isinstance(data, dict):
        raise ValueError(f"{source} must contain a mapping/object at the top level")
    return data


def dump_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def write_json(path: str | Path, data: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(dump_json(data), encoding="utf-8")


def iter_data_files(path: str | Path) -> list[Path]:
    root = Path(path)
    if root.is_file():
        return [root]
    if not root.exists():
        raise FileNotFoundError(root)
    return sorted(p for p in root.rglob("*") if p.suffix.lower() in DATA_EXTENSIONS)

