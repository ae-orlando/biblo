# Reference: parse format, validate meaning, replace deliberately

The reference uses DictReader with explicit encoding/newline handling and validates record structure/amount syntax. CSV parser errors are translated with their cause; missing-file/decoding failures are not silently turned into an empty report.

Output JSON is serialized before staging; a same-directory file is closed then replaced, with owned cleanup. This does not preserve all destination metadata or establish fsync-based durability/hostile-directory safety. Verification: `python3 90-tools/practice.py check py-files --reference`.
