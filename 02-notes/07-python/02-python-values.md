# Python 02 — values, names and explicit conversion

## Outcome

After [[01-python-execution]], distinguish text, integers, floating point, booleans and None; predict conversion behavior. Practice: py-basics, then boundary work in py-decisions.

```python
quantity = 3
label = "notebooks"
enabled = False
missing = None
print(type(quantity).__name__, repr(label))  # int 'notebooks'
print(f"{quantity} {label}")                 # 3 notebooks
```

Names refer to objects. Reassigning a name does not rewrite every other name; mutating a shared object can affect several names, which [[05-python-collections]] demonstrates. A type tells you which operations make sense. '3' + '2' joins text; 3 + 2 adds integers; mixing those operands is not implicit string-to-number validation.

## Numbers and domain choices

int supports arbitrarily large integer values subject to available memory. / returns a floating-point quotient; // uses floor division (including for negatives); % gives a remainder. float is binary floating point, so 0.1 + 0.2 is not exactly 0.3.

For the first receipt/expense exercises, use integer minor units such as cents. Real currencies and financial products can need different scales and explicit decimal/rounding rules. A later database or JSON consumer can impose a smaller range than Python's integer type.

bool represents True/False and is a subclass of int: isinstance(True, int) is true. If a contract requires a count rather than a boolean, type(value) is int is a deliberate stricter check—not a rule that every subclass should always be rejected.

## Text and conversion

Strings are immutable. strip() returns text without edge whitespace; it does not change the original. len() counts Python string code points, not user-perceived grapheme clusters or encoded UTF-8 bytes.

```python
text = " 42 "
print(text.strip(), int(text))  # 42 42
print(bool("false"))           # True: nonempty text is truthy
```

Conversion is not your complete validation policy. int can accept surrounding whitespace, signs, underscores and non-ASCII decimal digits. The later py-validation lab intentionally permits a narrower syntax. None means absence; it is different from 0, False, an empty list and an empty string even though all are falsy.

## Practice

Complete py-basics without converting the integer result to text or float. Predict 7 / 2, 7 // 2 and -7 // 2. In scratch code compare type, repr, == and is None. Do not use is for general numeric/string equality.

Next: [[03-python-control-flow]]. Sources: [numbers/text](https://docs.python.org/3.14/tutorial/introduction.html), [built-in types](https://docs.python.org/3.14/library/stdtypes.html).
