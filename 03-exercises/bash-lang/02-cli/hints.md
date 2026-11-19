# Safe report CLI — progressive hints

1. Parse options into variables/arrays, then validate all required arguments and paths before creating output.
2. `IFS= read -r` preserves text. A final nonempty unterminated line needs an explicit loop condition.
3. Create a unique temporary file beside the destination, register EXIT cleanup, write completely, then rename. Handle INT/TERM with explicit exits; a returning cleanup handler alone does not terminate execution.
