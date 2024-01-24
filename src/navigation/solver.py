from functools import lru_cache

from navigation.models import Empire, GalaxyMap, MillenniumFalcon


def compute_arrival_odds(
    falcon: MillenniumFalcon,
    empire: Empire,
    galaxy_map: GalaxyMap,
    captured_proba: float = 0.1,
) -> float:
    start_autonomy = falcon.autonomy
    max_proba = 0.0
    countdown = empire.countdown

    risky_days = {bh.day: bh.planet for bh in empire.bounty_hunters}

    @lru_cache(maxsize=128)
    def dfs(planet, day, autonomy, n_bounty):
        nonlocal max_proba
        if day > countdown:
            return 0.0

        if planet == falcon.arrival:
            # Compute success proba given how many BH encountered
            path_proba = 1 - sum(
                [(captured_proba) * (1 - captured_proba) ** i for i in range(n_bounty)]
            )
            max_proba = max(max_proba, path_proba)
            return

        # Encounter a bounty hunter !
        if day in risky_days and risky_days[day] == planet:
            n_bounty += 1

        # Two choices either I refuel in the same planet
        dfs(planet, day + 1, start_autonomy, n_bounty)

        # or explore the neighbors
        for travel_cost, nplanet in galaxy_map.get_neighbors(planet):
            # I have enough fuel to travel to the neighbor
            if autonomy >= travel_cost:
                dfs(nplanet, day + travel_cost, autonomy - travel_cost, n_bounty)

    dfs(falcon.departure, 0, falcon.autonomy, 0)
    return max_proba
