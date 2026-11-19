# Reference: composition and process contracts

main.py coordinates arguments, reporting functions, dry-run and expected error translation. reporting.py owns CSV loading, pure aggregation and staged output replacement. Repeated runs preserve input and produce the same report. A structured dry-run is a preview, not proof the destination will still be writable later.

The reference loads the small input in memory and is not a crash-durable financial system. An independent change request and evidence—not copying this package—complete the checkpoint. Verification: `python3 90-tools/practice.py check py-cli --reference`.
