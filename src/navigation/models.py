import os
import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush
from pprint import pprint
from typing import Any, Dict, List, Set


@dataclass
class BountyHunter:
    planet: str
    day: int


@dataclass
class Empire:
    countdown: int
    bounty_hunters: Dict[int, str]


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
