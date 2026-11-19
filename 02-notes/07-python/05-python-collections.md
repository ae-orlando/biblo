# Python 05 — lists, dictionaries, sets and ownership of data

## Outcome

Represent sequences, records and uniqueness; transform them without unintended mutation. Prerequisites: functions/control flow. Practice: py-records after [[06-python-errors]].

- list: ordered mutable sequence. Append adds an element; indexing can fail outside its range.
- tuple: immutable sequence container; referenced elements can still be mutable.
- dict: key/value mapping with unique hashable keys and insertion order. Missing indexing raises KeyError; get can supply a deliberate default.
- set: unique hashable values, without a presentation-order guarantee. Sort explicitly when output order matters.

```python
record = {"category": "travel", "cents": 120}
categories = {"travel", "office", "travel"}
print(record["category"], sorted(categories))
```

## Assignment is not a deep copy

If b = a refers to a list, both names refer to the same list. a.copy() copies the outer list, not every nested dictionary. Decide who may mutate each object. Returning new aggregate dictionaries avoids exposing a caller's original records as editable internal state.

Methods such as append and sort mutate and return None. sorted(values) returns a new sorted list. Do not port JavaScript assumptions about sort's return value into Python.

Comprehensions express simple transformations/filtering. Use a loop when several validation branches, state transitions or explanations make it clearer. A generator yields incrementally and can be consumed once; materializing every input into a list is not always appropriate for large files.

## Grouping algorithm

Validate each record, track seen IDs in a set, choose a category-normalization policy, update one aggregate per category, then emit newly created records in explicit order. Keep accumulators local to the call. A set/dict gives average efficient membership/lookup; a repeated list scan can do substantially more work as data grows. Measure a relevant input before optimizing.

## Practice and transfer

Complete py-records with whitespace/case normalization, duplicate IDs, zero amounts and rejected boolean amounts. Compare input before/after and call the function twice. Then add a refund policy and decide whether negative amounts are valid before editing arithmetic.

Teach back: why do tuples/frozen outer objects not guarantee deep immutability? When should missing dict data be an error instead of a default? Why is output sorting a contract decision rather than a side effect of iteration order?

Source: [Python data structures](https://docs.python.org/3.14/tutorial/datastructures.html).
