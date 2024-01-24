# Implementation details

## Solver

The problem in hands boils down to finding the path that maximizes the probability of getting to our destination before the countdown limit. To start, we can model the connection between planets as a **weighted graph** the weight of each edge represents the distance (in days) to do a Hyperspace jump. My first idea was to use a shortest-path algorithm like Djikstra on this graph, the sp algorithm would compute the shortest distance between the start and the destination. Now if we subtract the total days from our autonomy, we would have the minimum number of refuels needed to arrive at the destination. Because each refuel costs 1 day we can add it to the total and see if we make it before the countdown. If we can't make it in time to save the empire we can be sure that the odds of success are 0 because there is no faster way to get there!
All fine and dandy if not for bounty hunters! If I computed a probability of success for the shortest path while taking into account the bounty hunters we could cross on each planet along the way, there is no guarantee that it would be maximal. This means that there is a _longer_ path that we could take to make it in time and have a bigger success rate. At this point, I had two ideas:

1. Building a different graph that would correctly model the problem ie some way to reflect the probability of success to then run a greedy approach.
2. Computing the k-shortest path and then filtering to those that respect the limit countdown. Then compute the probability of success of each path and return the maximal

Looking at the 2nd solution, the structure of the problem became apparent, and the problem has an optimal substructure. The path that maximizes the probability of success contains another path that maximizes the probability of success within it. So we could model it as a dynamic programming problem. We run a DFS on the graph starting from the departure and either stay and refuel or move on the neighbors if we have enough fuel. If we exceed the time limit we return 0.0. If we arrive at the arrival planet we update the maximum probability. I used memoization on the `dfs` function to avoid recomputing each path once

## Architecture

CLI
Backend
Frontend

# Running the solution

1. Clone this repository and `cd` into it
   Create a Python virtual env. For example, you can use `venv` and activate it

   ```bash
   python -m venv env
   source env/bin/activate
   ```

2. Install the package. To run tests you should also install the dev dependencies

   ```
   pip install .
   # dev dependancies
   pip install -e ".[dev]"
   ```

## Running CLI version

The installed package defines a command line executable `give-me-the-odds`, you can run:

```bash
❯ give-me-the-odds examples/example2/millennium-falcon.json examples/example2/empire.json
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
                                                      You have a  81.00% chance to stop the Empire's from destroying Endor.
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

```

## Running the Web version

1. Before starting the API, first, modify the `.env` environment to have the correct

   ```env
   MILLENNIUM_FALCON_JSON=examples/example1/millennium-falcon.json
   ```

2. Start the front and back-end:
   ```env
    python -m uvicorn api:app
   ```
