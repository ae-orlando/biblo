# Bash capstone — prove a bounded tool, not the whole language

Complete the five Bash labs in [[practice-catalog]]. The executable capstone is [the inventory specification](../../03-exercises/bash-lang/05-capstone/README.md), ID `bash-capstone`.

## Compatibility contract

Target Bash 5+ and GNU find/stat/sort/sed on Linux. Associative arrays, mapfile delimiter handling and GNU utility flags are not supported by macOS's default Bash 3.2/BSD tools. A portable version is a separate implementation with its own compatibility tests, not a label applied to the same code.

## Required evidence

- The inventory meets its input/output, NUL-framing, sort, status and read-only contracts.
- Static checks are clean or each deliberate diagnostic is justified; behavioral tests pass.
- Explain the expansion order and status boundary of the trickiest line.
- Demonstrate a regression test catching one bug involving filenames, producer failure or ordering.
- State consistency limits for a changing filesystem and Bash integer overflow limits.

## Independent change request

Add `--include EXT` / `--exclude EXT` filtering with a documented interaction and empty-result policy. Preserve arbitrary filenames, deterministic ordering, explicit errors and no writes. Add tests before modifying the implementation.

Then design an Arch package-report variant using **captured pacman metadata fixtures first**. Keep live package installation, AUR review and service changes out of this language capstone. If a real installer follows, use [[30-script-workflow]] and VM evidence; never run it blindly on the host.

Use [[study-and-review]] to assess your own work. The supplied reference demonstrates one solution; neither it nor a clean linter establishes that you know every Bash feature.
