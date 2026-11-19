# Configuration — progressive hints

1. Pass the mapping in as a dependency. This makes tests independent of your shell and avoids inspecting real credentials.
2. Defaults apply when a key is absent, not when an explicitly supplied value is malformed. A nonempty string is truthy even if it says “false.”
3. Validate digits and range separately; map the two permitted DEBUG strings explicitly. Report the setting name, never the secret value.
