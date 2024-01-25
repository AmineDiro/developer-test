# TODO before submission:

- [x] Valid JSON with pydantic
- [x] Test function solver
- [x] Start API with the falcon and GALAXYMAP
- [x] API response with the odds
- [x] Refactor reading json file
- [x] Respond with a HTML reponse : templating or htmx ?
- [x] DB path : string): Path toward a SQLite database file containing the routes. The path can be either absolute or relative to the location of the millennium-falcon.json file itself.

- [ ] Deal with HTTP errors in Frontend
- [ ] Font serving in static ( font-family: 'SF Distant Galaxy');
- [ ] Write about the solution
- [ ] Close Button to go back

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
