# Python 06 — explicit errors and systematic debugging

## Outcome

Distinguish syntax, runtime, logic and environment failures; raise/catch only at a meaningful boundary. Prerequisites: functions and values. Practice: py-validation, py-records, then py-files.

An exception interrupts the current path and unwinds calls until a matching handler is found. TypeError can express an unsupported input type; ValueError can express a value outside the allowed format/domain. A caller can decide how to report an expected failure without making it success.

```python
def require_nonblank(text):
    if not isinstance(text, str):
        raise TypeError("expected text")
    if not text.strip():
        raise ValueError("text is required")
    return text.strip()
```

The lab has a different exact contract; do not assume this fragment implements every validator. int(text) alone is broader than a digits-only business policy. Avoid eval as an input parser: it executes Python expressions, not harmless data validation.

## Catch with a purpose

```python
try:
    count = int("bad")
except ValueError:
    print("That input is not an integer")
```

Catch an error you can recover from, translate or report appropriately. A blanket except/pass can hide missing permissions, corrupt data and programming defects. finally runs cleanup on ordinary unwinding; it is not a power-loss/SIGKILL guarantee. Context managers make ownership and cleanup more explicit for many resources.

Preserve a cause with raise NewError(...) from error when translating. Keep secrets out of messages/logs. A traceback contains the call path and relevant file/line context; inspect the failing value and the contract rather than assuming only its first/last line can matter.

## Practice loop

Implement py-validation: original type → complete trimmed syntax → conversion → range. Test an empty string, zero, suffix junk, underscores and non-ASCII digits. Predict which would be accepted by raw int before running.

Create a minimal reproducer for one failed assertion, make one hypothesis, collect a discriminating observation and repair the cause. Add a regression. A valid program that returns the wrong total is a logic bug even when no exception appears.

Next: [[07-python-files]]. Sources: [errors/exceptions](https://docs.python.org/3.14/tutorial/errors.html), [built-in exceptions](https://docs.python.org/3.14/library/exceptions.html).
