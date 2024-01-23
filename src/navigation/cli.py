import argparse

from rich.console import Console

from navigation.solver import compute_arrival_odds
from navigation.utils import read_empire_from_json, read_falcon_from_json

console = Console()


def main():
    parser = argparse.ArgumentParser(
        prog="runner",
        description="Finds the path of success !",
    )
    parser.add_argument(
        "millenium",
        help="millennium-falcon trajectory",
    )
    parser.add_argument(
        "empire",
        help="countdown and bounty_hunters",
    )
    args = parser.parse_args()

    empire = read_empire_from_json(args.empire)
    falcon, galaxy_map = read_falcon_from_json(args.millenium)

    with console.status("[bold green]Computing odds of success..."):
        odds = compute_arrival_odds(falcon, empire, galaxy_map)
        console.rule()
        console.print(
            f"You have a  {odds*100:.2f}% chance to stop the Empire's from destroying {falcon.arrival}.",
            style="bold green" if odds > 0.5 else "bold red",
            justify="center",
        )
        console.rule()
