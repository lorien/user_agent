from __future__ import annotations

import json
import pkgutil
from typing import Any, Dict, List, cast

# pylint: disable=deprecated-typing-alias
DataStore = List[Dict[str, Any]]
# pylint: enable=deprecated-typing-alias


def load_package_json_data(location: str) -> DataStore:
    return cast(
        DataStore, json.loads(cast(bytes, pkgutil.get_data("user_agent", location)))
    )


SMARTPHONE_DEV_IDS: DataStore = load_package_json_data("data/smartphone_dev_id.json")
TABLET_DEV_IDS: DataStore = load_package_json_data("data/tablet_dev_id.json")
