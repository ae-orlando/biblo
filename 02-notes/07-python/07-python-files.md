# Python 07 — paths, CSV, JSON and safe output

## Outcome

After collections/errors, read imperfect external data and write results without destroying a previous report on failure. Practice: py-files, then py-cli.

A path identifies a filesystem location, not an open file or a guarantee of access. Relative paths are interpreted from the process's working directory unless your code chooses a different base. Use pathlib to manipulate paths; keep a deliberate root for runtime data rather than scattering files beside imported source.

```python
from pathlib import Path
with Path("example.txt").open(encoding="utf-8") as source:
    text = source.read()
```

This fragment needs a file you deliberately created in your lab work directory. A with statement closes the owned resource on ordinary completion/error. A missing file, permission failure, invalid encoding and malformed content are different observations; do not turn every one into an empty successful result.

## Parse the format, then validate the records

CSV permits quoted delimiters and embedded newlines. Use csv.DictReader with an explicit encoding and newline=""; split(',') is not a CSV parser. Verify expected headers, missing/extra fields and each value. reader.line_num refers to physical lines, which need not equal record count.

JSON represents objects, arrays and primitive values. json.loads proving valid syntax does not prove the expected application shape or types. JSON encoding also needs a policy for nonfinite numbers, unsupported Python objects and interoperability ranges.

## Avoid partial replacement

For a small report in a private directory: validate inputs, serialize successfully, write a uniquely named temporary file beside the destination, close it, then use os.replace. Clean up your own temporary file on ordinary failure. Reject unintended input/output aliases and symlink output according to the contract.

Same-filesystem replacement gives an atomic namespace operation under the platform's guarantees; it is not a complete fsync-based durability, metadata-preservation or hostile-directory race-resistance protocol. Large reports may require streaming and a different resource policy.

## Practice

py-files uses a quoted-comma category and a category containing a newline. A serialization failure must leave the prior report unchanged and no temporary debris. Use fake data only; the checker creates/removes its own vault-local fixtures.

Transfer: add a row limit and define whether the whole import fails or valid rows are retained when one record is invalid. Explain the tradeoff before changing the loop. Record actual failure messages and what they establish.

Sources: [pathlib](https://docs.python.org/3.14/library/pathlib.html), [csv](https://docs.python.org/3.14/library/csv.html), [json](https://docs.python.org/3.14/library/json.html), [os.replace](https://docs.python.org/3.14/library/os.html#os.replace).
