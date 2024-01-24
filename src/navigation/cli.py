import argparse

from rich.console import Console

from navigation.models import Empire
from navigation.solver import compute_arrival_odds
from navigation.utils import read_json, start_millennium_falcon

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

    empire_data = read_json(args.empire)
    empire = Empire(**empire_data)

    # Build the galaxy map
    falcon, galaxy_map = start_millennium_falcon(args.millenium)

    with console.status("[bold green]Computing odds of success..."):
        odds = compute_arrival_odds(falcon, empire, galaxy_map)
        console.rule(
            style="bold green" if odds > 0.5 else "bold red",
        )
        console.print(
            f"You have a  {odds*100:.2f}% chance to stop the Empire's from destroying {falcon.arrival}.",
            style="bold green" if odds > 0.5 else "bold red",
            justify="center",
        )
        console.rule(
            style="bold green" if odds > 0.5 else "bold red",
        )
