# Reference: a small real package boundary

app.py composes a factory/store/router. catalog/domain.py owns in-memory behavior and a local lock; catalog/http.py owns schemas, dependency lookup and error translation. The domain imports no FastAPI. Each app's store is separate; tests can override the actual dependency.

This is one process's teaching state, not production persistence. Verification: `python3 90-tools/practice.py check api-dependencies --reference`. Folder quality also needs a responsibility/tradeoff explanation.
