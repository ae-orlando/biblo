# Reference: a process is an interface

The reference separates usage (`2`) from runtime/data failure (`1`) and success (`0`). It prints only the final result on stdout. `process.exitCode` lets output flush instead of forcibly terminating the process mid-write.

This small file-loading implementation intentionally has a bounded educational scope; large inputs need a streaming format and resource limits. Mutation to catch: logging progress to stdout or accepting a NULL value as numeric zero. Verification: `python3 90-tools/practice.py check js-cli --reference`.
