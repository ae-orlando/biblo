# Lab: inspect a process without changing it

**ID:** `linux-processes` · Linux `/proc` + Bash/awk · Outcome: collect process evidence instead of reflexively killing a PID.

Prerequisites: [[40-linux-processes]], [[11-bash-text-processing]].

Implement `work/main.sh POSITIVE_PID`. Read `/proc/PID/status` and print tab-separated `Name`, `Pid` and `PPid` records. Do not send signals, change priority or write to `/proc`.

Wrong argument count/nonpositive/nondigit PID → stderr/status `2`; missing or inaccessible process → stderr/status `1` with no success output. A PID is data, never a shell command to eval. The checker inspects its own live Python process and compares its parent ID.

```bash
python3 90-tools/practice.py start linux-processes
python3 90-tools/practice.py check linux-processes
```

Completion: explain PID versus parent/process group, why a process may disappear between observations, and why permission denial does not prove absence. Extend with elapsed CPU/memory evidence while documenting races and the limits of a single snapshot.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/linux-processes/explanation.md) · [proc_pid_status](https://man7.org/linux/man-pages/man5/proc_pid_status.5.html)
