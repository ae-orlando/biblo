# Python lab: CSV import and safe report replacement

**ID:** py-files. Prerequisites: collections/errors and [[07-python-files]].

Implement load_expenses(path): read UTF-8 CSV using its real format, requiring exactly category,amount_cents headers in that order. Category is nonblank after trimming; preserve internal commas/newlines. Amount is nonempty ASCII decimal digits, converted to nonnegative int. Reject missing/extra fields or invalid records with ValueError. Return [{'category':text,'cents':number},...]. Missing files remain FileNotFoundError; do not collapse all I/O/encoding failures into missing data.

Implement write_report(path,data): reject symlink output with ValueError, serialize valid JSON first, stage a unique file beside the destination and replace only after success. Preserve prior output after serialization failure and remove owned temporary debris. The parent must already exist.

```bash
python3 90-tools/practice.py start py-files
python3 90-tools/practice.py check py-files
```

Tests use quoted commas, embedded newlines, malformed rows and failed serialization. All fixtures are private vault-local temporary data.

Completion: explain CSV physical lines versus records and namespace atomic replacement versus crash durability. Extend with a documented row limit or whole-import/partial-import policy and tests. This private-directory exercise is not a privileged, hostile-path race-proof utility.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/py-files/explanation.md)
