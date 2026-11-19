# Reference: validation before conversion

`main.mjs` checks the original type, complete trimmed syntax and numeric safety separately. Leading zeros are explicitly allowed by this contract; signs and exponents are not. Another product could choose differently, but must state and test its policy.

Mutation to catch: replacing the syntax/range checks with `parseInt` accepts `'42px'` and can lose precision. Verification: `python3 90-tools/practice.py check js-values --reference`.
