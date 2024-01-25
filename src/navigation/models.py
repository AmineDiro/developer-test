import os
import sqlite3
from collections import defaultdict
from typing import Any, Dict, List, Set

from pydantic import BaseModel

Node = tuple[int, str]


class BountyHunter(BaseModel):
    planet: str
    day: int


class Empire(BaseModel):
    countdown: int
    bounty_hunters: List[BountyHunter]


class MillenniumFalcon(BaseModel):
    autonomy: int
    departure: str
    arrival: str
    routes_db: str


class GalaxyMap:
    def __init__(self, db_path: str):
        self.routes_db: sqlite3.Connection = self.connect(db_path)
        self.all_routes: List[Any] = self.get_routes()
        self.planets: Set[str] = self.get_planets()
        self.adj: Dict[str, List[Node]] = self.build_adj()

    def connect(self, db_path: str) -> sqlite3.Connection:
        assert os.path.exists(db_path)
        return sqlite3.connect(db_path)

    def get_routes(self) -> List[Any]:
        return list(self.routes_db.execute("SELECT * FROM routes;"))

    def get_planets(self) -> Set[str]:
        return set(
            [p for p, _, _ in self.all_routes] + [p for _, p, _ in self.all_routes]
        )

    def build_adj(self) -> Dict[str, List[Node]]:
        adj = defaultdict(list)

        for src_planet, dst_planet, cost in self.all_routes:
            # Two way routes
            adj[src_planet].append((cost, dst_planet))
            adj[dst_planet].append((cost, src_planet))

        return adj

    def get_neighbors(self, planet) -> Node:
        return self.adj[planet]
