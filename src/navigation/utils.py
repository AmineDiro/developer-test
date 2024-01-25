import json
import os
from typing import Tuple

from navigation.models import GalaxyMap, MillenniumFalcon


def absolute_db_path(db_path: str, falcon_path: str) -> str:
    if os.path.exists(db_path):
        return db_path
    return os.path.join(os.path.dirname(falcon_path), db_path)


def read_json(file_path) -> str:
    # TODO exception handling
    with open(file_path, "r") as file:
        return json.load(file)


def start_millennium_falcon(
    millennium_falcon_json,
) -> Tuple[MillenniumFalcon, GalaxyMap]:
    falcon_data = read_json(millennium_falcon_json)
    falcon = MillenniumFalcon(**falcon_data)
    db_path = absolute_db_path(falcon.routes_db, millennium_falcon_json)
    galaxy_map = GalaxyMap(db_path)
    return falcon, galaxy_map
