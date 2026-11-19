# Inventory — progressive hints

1. Create the mutable stock dictionary per instance, not as a shared mutable class attribute.
2. Return immutable item records or a suitably protected view; make snapshot dictionaries fresh.
3. Validate proposed changes before replacing stored state. A frozen dataclass is one suitable record representation, not the only possible implementation.
