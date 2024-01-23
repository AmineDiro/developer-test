import argparse

from navigation.solver import compute_arrival_odds
from navigation.utils import read_empire_from_json, read_falcon_from_json


def main():
    parser = argparse.ArgumentParser(
        prog="runner",
        description="Finds proba of success",
    )
    parser.add_argument(
        "-m",
        "--millenium",
        help="millennium-falcon trajectory",
        default="examples/example1/millennium-falcon.json",
    )
    parser.add_argument(
        "-e",
        "--empire",
        help="countdown and bounty_hunters",
        default="examples/example1/empire.json",
    )
    args = parser.parse_args()

    # main(args)

    empire = read_empire_from_json(args.empire)
    falcon, map = read_falcon_from_json(args.millenium)

    odds = compute_arrival_odds(falcon, empire, map)
    print(f"FINAL ODD: {odds}")
