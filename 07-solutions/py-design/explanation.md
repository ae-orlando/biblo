# Reference: explicit ownership of state

Each Inventory owns a private-by-convention dictionary. Frozen stock records prevent ordinary external assignment; snapshots copy the exposed fields. Reservation validates before replacing one record, so expected failures preserve state.

The underscore is a convention, not access-control security; frozen fields are not a universal deep-immutability guarantee. Real concurrent persistence requires a separate boundary. Verification: `python3 90-tools/practice.py check py-design --reference`.
