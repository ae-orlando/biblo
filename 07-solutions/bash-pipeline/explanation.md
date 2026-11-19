# Reference: success output is a commitment

The awk program validates records and accumulates counts, then emits only if no error was seen. Invalid records identify their line on stderr. The shell returns the parser's status rather than appending an always-successful command.

Mutation to catch: printing counts before discovering a bad final record, or ending with `... | sort` without preserving the parser's failure. Verification: `python3 90-tools/practice.py check bash-pipeline --reference`.
