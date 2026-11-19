# Lab: a file-report CLI with an error contract

**ID:** `js-cli` · Outcome: make a small tool composable through stdout, stderr and exit status.

Prerequisites: [[06-js-destructuring-modules]], [[10-js-node-scripts]], [[12-js-errors-regex]].

## Contract

Implement `work/main.mjs`:
- `node main.mjs FILE.json` reads a JSON array of `{label,value}` records. Each label is a nonblank string; each value is a finite number. Reject malformed data and a nonfinite sum.
- Print exactly one JSON result to stdout: `{count,total}`. An empty array returns `{count:0,total:0}`. Input files are read-only.
- `--help`: usage on stdout, no stderr, exit `0`.
- Missing/extra arguments or unknown long option: usage on stderr, no stdout, exit `2`.
- I/O, JSON or record failure: useful stderr, no stdout, exit `1`.

For values `2` and `-0.5`, expect `{"count":2,"total":1.5}`. This is a generic numerical report, not a currency-precision model.

```bash
python3 90-tools/practice.py start js-cli
python3 90-tools/practice.py check js-cli
```

Tests create their own spaced-path fixtures and remove only those fixtures. They invoke your program as a subprocess rather than inspecting source text.

Completion: explain the error boundaries, then add a validated `--min-value` filter without mixing logs into JSON output. Test misuse as well as success.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/js-cli/explanation.md) · [Node fs](https://nodejs.org/docs/latest-v24.x/api/fs.html)
