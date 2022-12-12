from __future__ import annotations

import json
import os
from typing import Any

PACKAGE_DIR: str = os.path.dirname(os.path.realpath(__file__))


def load_json_data(rel_path: str) -> Any:
    path = os.path.join(PACKAGE_DIR, rel_path)
    with open(path, encoding="utf-8") as inp:
        return json.load(inp)


SMARTPHONE_DEV_IDS: list[dict[str, Any]] = load_json_data("data/smartphone_dev_id.json")
TABLET_DEV_IDS: list[dict[str, Any]] = load_json_data("data/tablet_dev_id.json")
