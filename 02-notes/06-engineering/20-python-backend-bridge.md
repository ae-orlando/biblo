# Python backend bridge — enough language to work deliberately

> This older compact bridge assumes some programming familiarity and is **not** your entry point. You have stated no Python knowledge: follow [[python-learning-path]] instead. Continue toward [[fastapi-learning-path]], not an obligatory Django/current-project branch. This page is retained as a short reference.

## Outcome and prerequisites

After basic functions/control flow in any language, read and write small Python modules with explicit inputs, errors and tests. Complete `python-config` before assuming readiness for Django. Python 3.11+ is the lab baseline; the current environment is recorded separately.

## Core mechanisms

Python indentation defines suites; names refer to objects. Lists/dicts are mutable and assignment does not deep-copy them. A function should return a value or raise a deliberate exception, not silently guess after invalid input. Type annotations document/check intent through tooling; they do not automatically validate runtime input.

```python
def require_name(record):
    name = record.get('name', '').strip()
    if not name:
        raise ValueError('name is required')
    return name
```

This fragment assumes a mapping with a string value; state that assumption or validate it when inputs are untrusted. Like JavaScript, Python has truthiness traps: bool('false') is True. Parse configuration booleans according to an explicit accepted vocabulary.

Modules export names by definition; importing runs their top-level code. Put executable-only work under `if __name__ == '__main__':`. Prefer passing dependencies such as an environment mapping instead of reading global state inside every function.

## Resource and error boundaries

Use context managers for owned resources and catch only errors your layer can handle:

```python
from pathlib import Path
def read_text(path):
    try:
        return Path(path).read_text(encoding='utf-8')
    except FileNotFoundError:
        return None
```

This intentionally leaves decoding/permission failures visible. Do not collapse them into “missing.” For an opened file/connection, use a with block or a finally appropriate to its API. Do not log secrets in exception messages.

## Environment discipline

The standard-library lab needs no package installation. For a future project, choose a project-local virtual environment and declare/pin dependencies intentionally; never sudo pip install. Activation changes command lookup, not the fact that another interpreter can still be invoked explicitly. Project tooling/caches must stay within the authorized workspace.

## Practice and transfer

Use `python-config`: validate a mapping, distinguish missing from invalid values, convert deliberately, preserve the mapping and avoid token leakage. Read its unittest cases before implementing. Then extend with a deployment-mode enum and an explicit timezone/config policy. Explain how this unit remains independent of real os.environ and Django settings.

Continue to [[30-django-auth-bridge]] only when you can test and explain a small module independently.

Sources: [Python tutorial](https://docs.python.org/3/tutorial/), [modules](https://docs.python.org/3/tutorial/modules.html), [errors](https://docs.python.org/3/tutorial/errors.html), [venv](https://docs.python.org/3/library/venv.html).
