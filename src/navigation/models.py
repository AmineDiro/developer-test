import os
import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Set


@dataclass
class Empire:
    countdown: int
    bounty_hunters: Dict[int, str]


@dataclass
class MillenniumFalcon:
    autonomy: int
    departure: str
    arrival: str


class GalaxyMap:
    def __init__(self, db_path: str):
        self.routes_db: sqlite3.Connection = self.connect(db_path)
        # TODO: Define route struct
        self.all_routes: List[Any] = self.get_routes()
        self.planets: Set[str] = self.get_planets()
        self.adj: Dict[str, List[Any]] = self.build_adj()

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
            # Two way routes
            adj[src_planet].append((cost, dst_planet))
            adj[dst_planet].append((cost, src_planet))

        return adj

    def get_neighbors(self, planet):
        return self.adj[planet]
