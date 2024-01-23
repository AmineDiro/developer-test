import json
import os
from typing import Tuple

from navigation.solver import Empire, GalaxyMap, MillenniumFalcon


def read_falcon_from_json(file_path) -> Tuple[MillenniumFalcon, GalaxyMap]:
    with open(file_path, "r") as file:
        json_data = json.load(file)

    db_path = os.path.join(os.path.dirname(file_path), json_data["routes_db"])

    galaxy_map = GalaxyMap(db_path)

    falcon = MillenniumFalcon(
        autonomy=json_data["autonomy"],
        departure=json_data["departure"],
        arrival=json_data["arrival"],
    )
    return falcon, galaxy_map


def read_empire_from_json(file_path) -> Empire:
    with open(file_path, "r") as file:
        json_data = json.load(file)
    countdown = json_data["countdown"]
    bounty_hunters_data = json_data["bounty_hunters"]
    bounty_hunters = {bh["day"]: bh["planet"] for bh in bounty_hunters_data}
    return Empire(countdown=countdown, bounty_hunters=bounty_hunters)
