# Lab: repair only a marked permissions sandbox

**ID:** `linux-permissions` · Linux + Bash · Outcome: apply least-privilege modes without using sudo or broad recursive chmod.

Prerequisites: [[30-linux-permissions]], [[03-quoting-splitting-globbing]].

Implement `work/main.sh DIR`. The checker creates a fake directory with `.vault-permissions-lab` containing `practice-only`, subdirectories public/private/bin, and files private/token and bin/report.sh.

Validate the marker and all required non-symlink directories/files **before changing anything**. Missing marker or any symlinked required entry must fail nonzero. Never recurse through an arbitrary tree.

Set public `755`, private `700`, bin `750`, private/token `600`, bin/report.sh `750`. Preserve contents and ownership. Repeating the operation is safe. The marker reduces accidental misuse; it is not a security boundary against malicious concurrent path changes.

```bash
python3 90-tools/practice.py start linux-permissions
python3 90-tools/practice.py check linux-permissions
```

Fixtures are generated and removed automatically inside `.practice-runtime/checks/`. Do not pass your home directory, real SSH keys or system directories to this script.

Completion: explain directory execute versus read permission and calculate defaults using a bitmask, not subtraction. Extend with an explicit group-sharing policy and explain why chmod cannot change ownership.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/linux-permissions/explanation.md) · [Arch permissions](https://wiki.archlinux.org/title/File_permissions_and_attributes)
