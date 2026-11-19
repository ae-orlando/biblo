# Lab: worker lifecycle and signal cleanup

**ID:** `bash-jobs` · Bash 5+, Linux · Outcome: explicitly own and reap the workers you start.

Prerequisites: [[08-bash-functions-scope]], [[10-bash-traps-jobs]], [[14-set-shopt-strict-debug]].

Implement `work/main.sh WORKDIR` in an existing private scratch directory. Create a unique empty temporary subdirectory and start two `sleep 60` workers. Print one readiness line:

`READY<TAB>absolute-temporary-directory<TAB>worker1-PID<TAB>worker2-PID`

Wait for a line on stdin. `done` causes normal exit `0`. TERM causes exit `143`. On either path, terminate and reap your workers and remove your own empty scratch directory. Do not kill unrelated processes or remove broad paths. Invalid readiness/input must not pretend success.

```bash
python3 90-tools/practice.py start bash-jobs
python3 90-tools/practice.py check bash-jobs
```

Tests run the process in its own group, wait for readiness, exercise normal/TERM exits and check worker cleanup. They do not send KILL as a normal exercise.

Completion: explain why `trap cleanup TERM` can return to normal execution, why `wait` matters, and why no shell trap can guarantee cleanup after SIGKILL or power loss. Extend with one worker failure and an explicit parent failure policy.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/bash-jobs/explanation.md) · [Bash signals](https://www.gnu.org/software/bash/manual/html_node/Signals.html)
