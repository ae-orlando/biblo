# Count parser — progressive hints

1. Check the original type before any coercion. A valid zero must not be confused with failure.
2. Validate the complete trimmed string before converting. `parseInt` accepts a valid prefix followed by junk.
3. After a digits-only check, convert once and use `Number.isSafeInteger`. Distinguish type errors from the contract's format/range errors.
