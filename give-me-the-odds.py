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
from heapq import heappop, heappush
from pprint import pprint
from turtle import distance
from typing import Any, Dict, List, Set


@dataclass
class BountyHunter:
    planet: str
    day: int


@dataclass
class Empire:
    countdown: int
    bounty_hunters: List[BountyHunter]


def read_empire_from_json(file_path) -> Empire:
    with open(file_path, "r") as file:
        json_data = json.load(file)
    countdown = json_data["countdown"]
    bounty_hunters_data = json_data["bounty_hunters"]
    bounty_hunters = [
        BountyHunter(**hunter_data) for hunter_data in bounty_hunters_data
    ]
    return Empire(countdown=countdown, bounty_hunters=bounty_hunters)


class MillenniumFalcon:
    def __init__(self, autonomy, departure, arrival, routes_db):
        self.autonomy: int = autonomy
        self.departure: str = departure
        self.arrival: str = arrival
        self.routes_db: sqlite3.Connection = routes_db

        # TODO: Define route struct
        self.all_routes: List[Any] = self.get_routes()
        self.planets: Set[str] = self.get_planets()

        self.adj = self.build_adj()

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


def read_falcon_from_json(file_path) -> MillenniumFalcon:
    with open(file_path, "r") as file:
        json_data = json.load(file)

    db_path = os.path.join(os.path.dirname(file_path), json_data["routes_db"])
    assert os.path.exists(db_path)
    conn = sqlite3.connect(db_path)

    return MillenniumFalcon(
        autonomy=json_data["autonomy"],
        departure=json_data["departure"],
        arrival=json_data["arrival"],
        routes_db=conn,
    )


def compute_odds(falcon: MillenniumFalcon, empire: Empire) -> float:
    # Run djikstra to get the minium travel days
    # (not taking into account bountyhunters)
    minimum_travel_days = falcon.get_shortest_path()
    refuel_days = max(0, minimum_travel_days - falcon.autonomy)

    # if you can't make it in time even with travel return 0
    if minimum_travel_days + refuel_days > empire.countdown:
        return 0

    # Check for bounty hunters in the path and compute proba


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="runner",
        description="Finds proba of success",
    )
    parser.add_argument("millenium", help="millennium-falcon trajectory")
    parser.add_argument("empire", help="countdown and bounty_hunters")
    args = parser.parse_args()

    empire = read_empire_from_json(args.empire)
    falcon = read_falcon_from_json(args.millenium)

    compute_odds(falcon, empire)
