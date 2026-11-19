# Reference: validation before conversion

The reference checks the original type, trimmed nonempty ASCII decimal syntax and domain bound separately. It deliberately rejects underscores/signs that int can accept. Format/range failures are ValueError; unsupported input types are TypeError.

Verification: `python3 90-tools/practice.py check py-validation --reference`. Explain the contract before adapting it; a different product may reasonably permit a different numeric format.
