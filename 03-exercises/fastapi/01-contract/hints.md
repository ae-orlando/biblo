# API contract — progressive hints

1. A factory returns an app; it does not start a network server when imported.
2. Pydantic defaults can convert inputs. Use explicit strict/range/extra-field rules matching the contract.
3. Separate input/output schemas and assert exact successful representations as well as rejected requests. A rendered docs page is not proof of correct behavior.
