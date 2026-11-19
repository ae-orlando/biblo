# Service incidents — offline reasoning and VM-only practice

## Outcome and prerequisites

After [[40-linux-processes]], [[30-linux-permissions]] and [[60-linux-networking]], distinguish a failed unit, crashed process, missing listener, denied file and application error. The automated Linux labs supply prerequisites, not evidence that this whole unit is complete.

## Read the evidence before changing state

systemctl status is a summary; inspect the unit, effective drop-ins, environment source and journal for the relevant boot/time. A unit can be enabled but inactive, active but unhealthy, or repeatedly restarting. A successful TCP connection does not establish that the application returns correct HTTP behavior.

Use read-only commands with the correct system/user manager:

```bash
systemctl --user --failed --no-pager
systemctl --user cat YOUR-UNIT.service
journalctl --user -u YOUR-UNIT.service --since today --no-pager
```

YOUR-UNIT is a placeholder for an actual unit you own. Do not paste a production service name and restart it as a diagnostic guess. Unit files are not interactive shell scripts; expansion, PATH, working directory and redirection rules differ.

## Offline case

A training unit declares `WorkingDirectory=/srv/training` and `ExecStart=/srv/training/venv/bin/python app.py`. Its journal reports `Failed at step CHDIR spawning ...: No such file or directory`.

Write answers before consulting the manual:
1. Which step failed before Python could run? What observation distinguishes missing directory from missing Python?
2. Which unit/drop-in, path-component and ownership observations would you collect?
3. Why would reinstalling Python or opening a firewall port fail to address this evidence?
4. How would you verify the repair and avoid weakening unrelated permissions?

Then change the evidence to status 203/EXEC, then a running process returning HTTP 503. Explain the different layer and next observation in each case.

## VM-only worksheet

Use a disposable VM with a snapshot, fake files and no real credentials. Create a small loopback-only HTTP service and record its baseline unit/log/response. Introduce **one** fault at a time: wrong working directory, inaccessible config, missing required environment variable, occupied port, failing application handler. For each:

- Preserve the error and one hypothesis.
- Show the smallest relevant observation and root-cause reasoning.
- Make one narrow repair, verify the intended behavior and check for regressions.
- Restore the snapshot/baseline before the next incident.

Installing a unit, daemon-reload, enabling/restarting it and editing host networking are not automatically authorized on your real machine. Never expose an unauthenticated training server to a LAN/internet interface. A VM/network boundary itself needs correct configuration.

## Completion and transfer

Produce an incident report with observations, cause, repair, verification, recovery and prevention. Explain why enabled != active != healthy. Transfer: the process starts manually but fails under systemd; investigate differences in environment, identity, working directory, filesystem access and readiness rather than assuming systemd is broken.

Sources: [systemd.service](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html), [systemd.exec](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html), [journalctl](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html).
