# Reference: a local loop invariant

Each accumulator describes the processed prefix of input and starts at zero. The reference reads elements without changing the input and returns only after processing all of them. A new call receives a fresh local accumulator.

Comprehensions/builtins could express these operations too; readable loops are appropriate learning and production tools. Verification: `python3 90-tools/practice.py check py-loops --reference`.
