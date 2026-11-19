# Schema lab — progressive hints

1. **Model:** the FK belongs on the many side. A profile's user key must also be unique.
2. **Invariant:** SQL `CHECK` rejects false, not unknown. Add nullability separately. A canonical string can be compared with its normalized form.
3. **Implementation direction:** use an identity PK for generated entities and a shared PK/FK for profiles. Choose delete actions explicitly on child FKs. Consult the reference only after predicting the failing test.
