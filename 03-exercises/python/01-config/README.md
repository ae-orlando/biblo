# Lab: explicit configuration with safe errors

**ID:** `python-config` · Python 3.11+ · Outcome: validate configuration without hidden global state or secret leakage.

Prerequisite: [[20-python-backend-bridge]]. Export `load_config(env)` from `work/main.py`. The mapping contains strings, as environment variables normally do; do not read or mutate real `os.environ`.

- Require nonblank `TRAINING_TOKEN`, trim it and return it as `token`. Use fake values only.
- Optional `PORT` defaults to `'8000'`. Accept ASCII decimal digits representing 1..65535, return integer `port`. Reject underscores, decimal fractions and out-of-range values.
- Optional `DEBUG` defaults to `'false'`; permit only exact `'true'`/`'false'`, return boolean `debug`.
- Invalid configuration raises `ValueError` identifying the setting without including its value. Do not silently use defaults for explicitly invalid values.

Example: `{'TRAINING_TOKEN':' fake ','PORT':'9000','DEBUG':'true'}` → `{'token':'fake','port':9000,'debug':True}`.

```bash
python3 90-tools/practice.py start python-config
python3 90-tools/practice.py check python-config
```

Completion: explain mapping access, explicit conversion, exceptions and why `bool('false')` is true. Extend with a validated enum and tests proving independent calls do not share configuration.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/python-config/explanation.md) · [Python exceptions](https://docs.python.org/3/tutorial/errors.html)
