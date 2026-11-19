# Python checkpoint — a tool you can maintain independently

## Prerequisites and deliverable

Complete the synchronous units through files, modules, objects and testing. Async, FastAPI and a database are not required. The executable checkpoint is `py-cli` in [[practice-catalog]].

Read a CSV expense file, validate it, normalize/group categories, generate deterministic JSON and replace an output safely. Compose your own tested functions into an entry point and reusable module; do not import 07-solutions. Support help, deliberate usage/runtime failures and a genuinely non-writing dry-run.

## Evidence beyond a green supplied check

- Explain the flow from argv to file parser to validated records to report to output.
- Preserve whitespace/CSV quoting correctly and explain the row/encoding failure contract.
- Show a regression catching an introduced bug and a rejected input leaving an older report intact.
- Run with a different input path/working directory; no hard-coded fixture answers or hidden environment dependencies.
- Document actual setup/run/check commands, supported schema and known limitations.

## Independent change request

Add refunds with an explicit sign/policy, or add a date range filter with strict calendar validation. Choose one, specify it before coding, update tests and keep the existing behavior correct. Do not merely rewrite the same solution from memory.

Then implement the existing python-config lab and explain why missing settings, invalid settings and secrets in error messages require different handling. Review Git fundamentals for preserving the working version before changes.

## Ready for the next stage when…

You can build, test, debug and explain this kind of unfamiliar small program using documentation but without a copied walkthrough. If not, diagnose the missing unit rather than moving on because every note was opened. This checkpoint is not a claim to mastery of every Python feature.

Next: HTTP foundations and SQL as needed, then [[fastapi-learning-path]]. For later app growth see [[web-app-structure]].
