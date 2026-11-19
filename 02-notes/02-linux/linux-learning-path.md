# Linux learning path — evidence before intervention

Linux operations, Bash semantics and automation are related but distinct. Use [[00-how-to-use-track]] for expansion/quoting; use this path to diagnose an operating system; use [[30-script-workflow]] before automating privileged changes.

## Sequence

| Unit | Read | Evidence |
| --- | --- | --- |
| Orientation | [[00-linux-introduction]], [[10-linux-filesystem-navigation]] | Identify working directory, mount versus path, shell versus program, help source |
| Streams and files | [[20-linux-files-and-text]], [[03-quoting-splitting-globbing]] | `bash-quoting` and `bash-pipeline` in [[practice-catalog]] |
| Access | [[30-linux-permissions]] | `linux-permissions`: narrowly repair a marked sandbox without sudo |
| Processes | [[40-linux-processes]], [[10-bash-traps-jobs]] | `linux-processes` plus `bash-jobs`: inspect, then manage only owned workers |
| Networking | [[60-linux-networking]], [[00-web-foundations]] | `linux-network`: distinguish HTTP response from transport failure |
| Packages/services | [[50-arch-packages]], [[70-linux-shell-workflow]], [[80-linux-service-incidents]] | Read-only diagnosis, then the separately gated VM worksheet |

The checker writes only vault-local test artifacts. It does not install host packages, change permissions outside fixtures, alter services or modify dotfiles. Reference snippets elsewhere containing sudo, package installation, SSH configuration or service changes are **administration material**, not course setup commands.

## Cumulative incident

A local application cannot read a file and its health URL fails. Preserve the exact error, classify file/path access versus process/listener versus HTTP behavior, collect a minimal relevant observation, state a hypothesis, test it and change only what the evidence supports. Save before/after observations and one alternative cause you ruled out.

Do not fix every permission with 777, kill every process matching a word, enable random services or disable a firewall. A repair without an explanation and verified outcome is not completion.

## Progression beyond the host-safe labs

Use [[80-linux-service-incidents]] for logs, units, environment and dependency diagnosis. Installation, boot, SSH/firewall and display-manager changes require a disposable VM snapshot or a separately authorized real system. The rebuild provides a worksheet, not a claim that VM administration has been executed.

Apply [[study-and-review]] to correctness, safety, observations, recovery and transfer. Preserve your existing [[90-linux-protips]] as experience; do not generate fake “I fixed this” entries.
