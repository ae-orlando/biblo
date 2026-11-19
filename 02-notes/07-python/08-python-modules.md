# Python 08 — modules, packages and environments

## Outcome

Separate reusable calculations from executable effects and identify the interpreter/dependencies actually used. Prerequisites: functions, files and errors. Practice: py-cli; see [[web-app-structure]] after a real need to split modules appears.

A module is importable code with its own namespace. Importing executes its top-level statements and normally caches the module in that interpreter. Do not open a production database, send email, start a server or parse command-line arguments merely because another file imports a helper.

```python
def main():
    print("Explicit execution")

if __name__ == "__main__":
    main()
```

When run as a script, `__name__` is `__main__`; when imported normally it names the module. The guard keeps executable-only work out of import. A conventional package contains `__init__.py`; namespace packages are a separate mechanism, not a reason to guess at import behavior.

## Give imports a direction

Let the entry point coordinate parsing, data loading, calculation and output. Reusable domain logic should not import the CLI or web router that calls it. Circular imports often reveal an unclear dependency boundary. Avoid naming your module csv.py, json.py or typing.py when it would shadow the standard module you intend to import.

Execution style affects import lookup. For a packaged application, choose/document a supported module or installed entry point instead of sprinkling sys.path modifications throughout application code. The vault's test harness uses an explicit target loader; that is harness plumbing, not the ideal layout of every application.

## Environments and dependencies

An interpreter has an associated package environment. A virtual environment keeps project dependencies separate; activation changes command lookup, not the meaning of every python command on the system. Inspect sys.executable and use the selected interpreter's -m pip when deliberately installing.

The beginner labs need no extra packages. Later FastAPI/browser checks use marked environments under .tools/ and a documented installer. Do not use sudo pip, silently download packages through unrelated commands or assume a top-level dependency pin locks all transitive versions.

## Practice and transfer

Split the reporting CLI into an entry point and reporting module. Prove importing the reusable module does not print, parse argv or create an output file. Run checks from a different working directory with explicit input/output paths and explain which paths are data versus import locations.

Sources: [modules/packages](https://docs.python.org/3.14/tutorial/modules.html), [venv](https://docs.python.org/3.14/library/venv.html), [Python packaging guide](https://packaging.python.org/en/latest/).
