# Files — progressive hints

1. split(',') cannot handle quoted delimiters/newlines. Use the CSV module and newline='' with an explicit encoding.
2. Validate headers and each parsed record; conversion alone does not enforce the digits-only policy.
3. Serialize before touching the old output. A unique same-directory temp plus os.replace and finally cleanup supports this exercise's ordinary-failure contract, not universal durability/security.
