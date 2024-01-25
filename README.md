# Implementation details

## Computing odds:

The problem in hands boils down to finding the path that maximizes the probability of getting to our destination before the countdown limit. We can model the connection between planets as a **weighted graph** the weight of each edge represents the distance (in days) to do a Hyperspace jump.
My first idea was to use a shortest-path algorithm like Djikstra on this graph, the sp algorithm would compute the shortest distance between the start and the destination. Now if we subtract the total days from our autonomy, we would have the minimum number of refuels needed to arrive at the destination. Each refuel costs 1 day, so we can add it to the total and see if we make it before the countdown. If we can't make it in time to save the empire we can be sure that the odds of success are 0 because there is no faster way to get there!

All fine and dandy if not for bounty hunters! If I computed a probability of success for the shortest path while taking into account the bounty hunters we could cross on each planet along the way, there is no guarantee that it would be maximal. This means that there is a _longer_ path that we could take to make it in time and have a bigger success rate. At this point, I had two ideas:

1. Building a different graph that would correctly model the problem ie some way to reflect the probability of success to then run a greedy approach.
2. Computing the k-shortest path and then filtering to those that respect the limit countdown. Then compute the probability of success of each path and return the maximal

Looking at the 2nd solution, the structure of the problem became apparent. We can see that greedy approaches can't work. The good news is that the problem has an optimal substructure: the path that maximizes the probability of success contains other paths that maximize the probability of success within it. We can use dynamic programming to solve the problem. The solver does a (recursive) depth first on the graph starting from the departure. On each planet, we either stay and refuel or move on the neighbors if we have enough fuel. If we exceed the time limit we return 0.0. If we arrive at the arrival planet we update the maximum probability. I used memoization on the `dfs` function to avoid recomputing each path.

## Architecture

- The input `json` files are first validated using `pydantic` to models we can reuse in both the CLI and the Web.
- Build a graph data structure from the sqlite database: `GalaxyMap`
- The core logic for computing odds is encapsulated in the `solver` module.

**CLI**:

- Used std `argparse` to parse arguments and `rich` for colored output.

**Backend**

- Used `fastAPI` framework.
- Used the builtin `sqlite3` Python lib.

**Frontend**

- Used Jinja2 templates and with FastAPI
- I also used `HTMX` as an efficient way to build dynamic web applications.
- Custom Star Wars font of course 😄

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

## Running CLI

The installed package defines a command line executable `give-me-the-odds`, you can run:

```bash
give-me-the-odds examples/example2/millennium-falcon.json examples/example2/empire.json

You have a  81.00% chance to stop the Empire's from destroying Endor.
```

## Running the Web version

1. Before starting the API, modify the `.env` file to have the correct

   ```env
   MILLENNIUM_FALCON_JSON=examples/example1/millennium-falcon.json
   ```

2. Start the front and back-end:
   ```env
    python -m uvicorn api:app --port 8000 --host 0.0.0.0
   ```
3. Navigate to `http://localhost:8000` to save the galaxy!

## Running tests

To run the tests you to first install the `dev` dependencies and then run:

```bash
developer-test  🍣 solution 📝 ×4🛤️  ×2via 🐍 v3.10.8 (env)
❯ pytest tests -s -v
================================== test session starts ==================================
platform darwin -- Python 3.10.8, pytest-7.4.4, pluggy-1.3.0 -- /Users/aminedirhoussi/Documents/coding/developer-test/env/bin/python
cachedir: .pytest_cache
rootdir: /Users/aminedirhoussi/Documents/coding/developer-test
plugins: anyio-4.2.0
collected 4 items

tests/test_solver.py::test_solver[examples/example1/millennium-falcon.json-examples/example1/empire.json-examples/example1/answer.json] PASSED
tests/test_solver.py::test_solver[examples/example2/millennium-falcon.json-examples/example2/empire.json-examples/example2/answer.json] PASSED
tests/test_solver.py::test_solver[examples/example3/millennium-falcon.json-examples/example3/empire.json-examples/example3/answer.json] PASSED
tests/test_solver.py::test_solver[examples/example4/millennium-falcon.json-examples/example4/empire.json-examples/example4/answer.json] PASSED
```
