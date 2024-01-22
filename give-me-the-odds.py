#!/usr/bin/env
"""
The command-line interface should consist of an executable that takes 2 files 
paths as input (respectively the paths toward the `millennium-falcon.json` 
and `empire.json` files) and prints the probability of success as 
a number ranging from 0 to 100.
 give-me-the-odds example1/millennium-falcon.json example1/empire.json
"""

import argparse
import json
import os
import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from heapq import heappop, heappush
from pprint import pprint
from typing import Any, Dict, List, Set, Tuple


@dataclass
class BountyHunter:
    planet: str
    day: int


@dataclass
class Empire:
    countdown: int
    bounty_hunters: Dict[int, str]


def read_empire_from_json(file_path) -> Empire:
    with open(file_path, "r") as file:
        json_data = json.load(file)
    countdown = json_data["countdown"]
    bounty_hunters_data = json_data["bounty_hunters"]
    bounty_hunters = {bh["day"]: bh["planet"] for bh in bounty_hunters_data}
    return Empire(countdown=countdown, bounty_hunters=bounty_hunters)


class GalaxyMap:
    def __init__(self, db_path: str):
        self.routes_db: sqlite3.Connection = self.connect(db_path)
        # TODO: Define route struct
        self.all_routes: List[Any] = self.get_routes()
        self.planets: Set[str] = self.get_planets()
        self.adj = self.build_adj()

    # TODO : handle  exceptions
    def connect(self, db_path) -> sqlite3.Connection:
        assert os.path.exists(db_path)
        return sqlite3.connect(db_path)

    def get_routes(self):
        return list(self.routes_db.execute("SELECT * FROM routes;"))

    def get_planets(self):
        return set(
            [p for p, _, _ in self.all_routes] + [p for _, p, _ in self.all_routes]
        )

    def build_adj(self):
        adj = defaultdict(list)

        for src_planet, dst_planet, cost in self.all_routes:
            adj[src_planet].append((cost, dst_planet))
            adj[dst_planet].append((cost, src_planet))

        return adj

    def get_neighbors(self, planet):
        return self.adj[planet]


@dataclass
class MillenniumFalcon:
    autonomy: int
    departure: str
    arrival: str

    def get_shortest_path(self) -> int:
        """djikstra's shortest path algo"""

        costs = {vertex: float("infinity") for vertex in self.adj}
        costs[self.departure] = 0

        # min- heap
        pprint(self.adj)
        q = [(0, self.departure)]

        while q:
            curr_cost, curr_node = heappop(q)

            if curr_cost > costs[curr_node]:
                continue

            for travel_cost, neighbor in self.adj[curr_node]:
                total_cost = travel_cost + curr_cost
                print(f"FROM {curr_node} to {neighbor} costs {total_cost}")
                if total_cost < costs[neighbor]:
                    costs[neighbor] = total_cost
                    heappush(q, (total_cost, neighbor))
                    # print("q", q)
                    print("costs", costs)

        return costs[self.arrival]


def read_falcon_from_json(file_path) -> Tuple[MillenniumFalcon, GalaxyMap]:
    with open(file_path, "r") as file:
        json_data = json.load(file)

    db_path = os.path.join(os.path.dirname(file_path), json_data["routes_db"])

    map = GalaxyMap(db_path)

    falcon = MillenniumFalcon(
        autonomy=json_data["autonomy"],
        departure=json_data["departure"],
        arrival=json_data["arrival"],
    )
    return falcon, map


def compute_arrival_odds(
    falcon: MillenniumFalcon,
    empire: Empire,
    map: GalaxyMap,
    captured_proba: float = 0.1,
) -> float:
    start_autonomy = falcon.autonomy
    max_proba = 0.0
    countdown = empire.countdown

    @lru_cache(maxsize=None)
    def dfs(planet, day, autonomy, n_bounty):
        nonlocal max_proba
        if day > countdown:
            return 0.0

        if planet == falcon.arrival:
            # Compute proba how many BH I have encountered
            path_proba = 1 - sum(
                [(captured_proba) * (1 - captured_proba) ** i for i in range(n_bounty)]
            )
            max_proba = max(max_proba, path_proba)
            return path_proba

        # Encounter a bounty hunter !
        if day in empire.bounty_hunters and empire.bounty_hunters[day] == planet:
            n_bounty += 1

        # Two choices either I refuel in the same planet
        dfs(planet, day + 1, start_autonomy, n_bounty)

        # or explore the neighbors
        for travel_cost, nplanet in map.get_neighbors(planet):
            # I have enough fuel to travel to the neighbor
            if autonomy >= travel_cost:
                dfs(nplanet, day + travel_cost, autonomy - travel_cost, n_bounty)

    dfs(falcon.departure, 0, falcon.autonomy, 0)
    return max_proba

    # Check for bounty hunters in the path and compute proba


if __name__ == "__main__":
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
