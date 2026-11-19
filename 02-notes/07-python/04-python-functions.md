# Python 04 — function contracts, scope and composition

## Outcome

After the small function primer and control-flow labs, separate inputs, returned values, side effects and failures. Use functions to express one understandable responsibility. Continue into py-validation after [[06-python-errors]].

A parameter is a name in a definition; an argument is the value passed by a call. return ends that call and sends a value to its caller. A function that reaches the end without return returns None. Local assignment normally binds a local name; reading/modifying shared state needs explicit thought.

```python
def greet(name, punctuation="!"):
    return f"Hello, {name}{punctuation}"

print(greet("Ana", punctuation="."))
```

Defaults are evaluated when the definition executes, not fresh on each call. A mutable default list can accidentally accumulate work from earlier calls. Use None as a sentinel and create a new object when missing; do not use an or default when an explicitly supplied empty collection is meaningful.

## Composition and boundaries

Prefer functions that receive values and return new values for calculation/validation. Keep reading files, printing, environment access and network operations at deliberate boundaries. A pure transformation is easier to test, but not every function must be pure; a useful program eventually performs effects.

Name the contract: allowed types/range/shape, output meaning, failure behavior and mutation policy. Type annotations do not enforce that contract at runtime. A function that reports failures with None needs callers to distinguish None from valid falsy results; exceptions can make invalid-input paths explicit once introduced.

Do not make a separate function for every line or one giant function for every responsibility. Extract a helper when its name/contract reduces reasoning or it is independently reusable/testable. Avoid hidden reads of global settings in the middle of calculations.

## Practice

Refactor one decisions/loops solution without changing its tests. Explain what the caller observes, including whether input is mutated. Write two calls with different data and prove they do not share accidental state. After learning exceptions, implement py-validation and distinguish format, type and range failures.

Retrieval: why does printing a result not satisfy a function return contract? When does a default object get created? What would change if a helper opened a file instead of receiving parsed records?

Sources: [defining functions/defaults](https://docs.python.org/3.14/tutorial/controlflow.html#more-on-defining-functions), [execution model](https://docs.python.org/3.14/reference/executionmodel.html).
