import os

import pytest

from navigation.models import Empire, GalaxyMap, MillenniumFalcon
from navigation.solver import compute_arrival_odds
from navigation.utils import absolute_db_path, read_json, start_millennium_falcon


@pytest.mark.parametrize(
    "falcon_json,empire_json,answer_json",
    [
        (
            "examples/example1/millennium-falcon.json",
            "examples/example1/empire.json",
            "examples/example1/answer.json",
        ),
        (
            "examples/example2/millennium-falcon.json",
            "examples/example2/empire.json",
            "examples/example2/answer.json",
        ),
        (
            "examples/example3/millennium-falcon.json",
            "examples/example3/empire.json",
            "examples/example3/answer.json",
        ),
        (
            "examples/example4/millennium-falcon.json",
            "examples/example4/empire.json",
            "examples/example4/answer.json",
        ),
    ],
)
def test_solver(falcon_json, empire_json, answer_json):
    empire_data = read_json(empire_json)
    answer = read_json(answer_json)["odds"]
    empire = Empire(**empire_data)

    falcon, galaxy_map = start_millennium_falcon(falcon_json)
    odds = compute_arrival_odds(falcon, empire, galaxy_map)

    assert odds == answer
