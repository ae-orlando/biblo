# Python capstone lab: maintainable expense-report CLI

**ID:** py-cli. Complete synchronous Python units through modules/files/testing first. This integrates mechanisms, not a web framework or current business project.

Implement work/main.py plus a reusable reporting module. Copy/adapt your own tested functions, never import the reference.

Contract: `python3 -B main.py SOURCE.csv --output REPORT.json [--dry-run]`. CSV uses category,amount_cents; validate like py-files, normalize categories with strip().lower(), count/sum rows, sort category output and emit:

```json
{"categories":[{"category":"travel","count":2,"cents":35}],"total_cents":35}
```

Success writes JSON safely and emits no stdout/stderr; invalid data/I/O → stderr/status 1, no partial success output, old report preserved. Usage errors → 2; --help → stdout/0. Input/output must differ. Dry-run prints JSON {'would_write':path,'report':report}, writes no report/temp data and leaves prior output unchanged; it does not prove later destination writability. -B avoids interpreter bytecode-cache writes during filesystem checks.

```bash
python3 90-tools/practice.py start py-cli
python3 90-tools/practice.py check py-cli
```

Completion: explain the complete data/error flow, catch a deliberate regression and meet [[12-python-capstone]]'s changed requirement independently. Document setup, schema, real checks and limitations.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/py-cli/explanation.md)
