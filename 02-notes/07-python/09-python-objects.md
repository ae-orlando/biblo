# Python 09 — classes, dataclasses and protected invariants

## Outcome

Use an object when state and operations form one useful responsibility; avoid classes merely to wrap every function. Prerequisites: dictionaries, functions and exceptions. Practice: py-design.

A class defines a type and its behavior; an instance owns its state. `self` is the explicit conventional name for the instance passed to an instance method. `__init__` initializes that instance. A mutable class attribute is shared; a dictionary assigned to self inside `__init__` belongs to that instance.

```python
class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1
        return self.value
```

Two Counter instances should not share a counter accidentally. A leading underscore signals an implementation detail by convention; it does not provide a security boundary.

## Records versus services

A dataclass can generate useful initialization/comparison/representation behavior for a record. frozen=True prevents ordinary field assignment, but referenced mutable objects can still change. Type annotations alone do not validate all constructor inputs.

Use a small record for returned stock snapshots and an Inventory object to enforce stock operations. Validate a proposed change before replacing stored state. Returning the actual mutable internal dictionary lets callers bypass the very invariant the methods were meant to protect.

Prefer composition over speculative inheritance: a repository can receive a connection/configuration dependency without becoming a subclass of the HTTP router. Add interfaces/protocols when interchangeable implementations/testing justify them, not as first-day architecture ceremony.

## Practice

py-design requires independent instances, immutable item views, fresh snapshots and unchanged state after a rejected reservation. Missing SKU and insufficient stock are different failures. A class used by multiple threads/processes needs a separate concurrency policy; this single-process domain exercise does not make in-memory state a production database.

Transfer: add stock replenishment with a validated positive quantity, then add tests proving failures preserve state and returned snapshots cannot mutate it. Explain why the same business invariant must also be enforced at the persistence boundary later.

Sources: [classes](https://docs.python.org/3.14/tutorial/classes.html), [dataclasses](https://docs.python.org/3.14/library/dataclasses.html).
