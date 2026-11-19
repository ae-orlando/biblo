---
created: 2026-10-08
updated: 2026-10-21
---

# 10 — Traps and Jobs

> Prerequisites: functions, exit statuses and redirections. Outcome: own, stop and reap workers while preserving exit status. Practice: `bash-jobs` in [[practice-catalog]].

## Mental model

Signals request actions; handlers can change the default. INT usually comes from Ctrl-C, TERM requests termination, and KILL cannot be caught. EXIT cleanup runs on ordinary shell-exit paths, not SIGKILL or power loss. A returning TERM handler can let execution continue. Background commands have inheritance/job-control rules, and wait collects their status.

## Traps
```bash
mkdir -p .practice-runtime/scratch
tmp=$(mktemp -d .practice-runtime/scratch/traps.XXXXXX)
cleanup() { rmdir -- "$tmp"; }  # empty private example directory only
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
trap -p INT                 # list: trap -- 'cmd' SIGINT
trap - INT                  # reset to default; trap '' INT ignores
trap -l                     # list all signal names/numbers (HUP INT QUIT ILL TRAP ABRT BUS FPE KILL USR1 SEGV ...)
```
Quote rule: **single-quote the body** so `$tmp` expands at FIRE time. Double quotes expand at DEFINITION time (usually empty/wrong). `trap ... ERR` needs `set -E` (`errtrace`) to inherit in functions/subshells and follows the same limits as `set -e` — usually noisy; EXIT-only is the standard. `trap ... DEBUG` fires before EVERY command (see note 14 tracing); `RETURN` fires on function return with `set -T` (`functrace`).

## Jobs
```bash
sleep 30 & pid=$!; echo "$pid"; kill "$pid"; wait "$pid" 2>/dev/null || true
sleep 2 & sleep 2 & wait        # wait for ALL
wait -n                         # wait for NEXT job only (bash 4.3+; loop for N-way parallel)
sleep 60 & sleep 61 & jobs      # listing tracked jobs does not require set -m
jobs -p; jobs -l                # PIDs only / full lines
kill %1; fg %1; bg %1           # %N jobspecs: kill/fore/background; %+ current, %- previous, %% current
disown -h %1                    # keep running after shell exits (no SIGHUP); checkjobs/huponexit control this
kill -l TERM; kill -TERM "$pid" # names; TERM→wait→KILL escalation (never -9 first)
```
kill defaults to TERM, but the target may ignore or handle it; verify the outcome. `wait "$pid"` returns the worker's status. With errexit, use an explicit conditional if failure is expected. Enabling job control changes process groups and permits fg/bg; it is not required merely to list or wait for a background job. Never signal a broad matching name when you own a precise child PID.

## Pitfalls

- `trap "rm -rf $tmp"` — expands NOW. Single quotes.
- `trap cleanup EXIT` with `cleanup` using unset vars under `set -u` — guard `"${tmp:?}"` or `[[ -n ${tmp:-} ]]`.
- `kill -9` first reflex corrupts state — TERM, wait, escalate only if ignored.
- Forgetting `wait` — background failures go unnoticed; script "succeeds" while workers died.

## Try it

```bash
bash -c 'm=at-def; trap '\''printf "value:%s\n" "$m"'\'' EXIT; m=at-fire'
bash -c 'sleep 5 & p=$!; echo "pid:$p"; kill "$p"; wait "$p" 2>/dev/null; echo "rc:$?"'
bash -c 'm=at-def; trap '\''echo $m'\'' EXIT; m=at-fire'
```

## Optional scratch drills (inside bash-jobs/work)

1. `tmp.sh`: create a private empty scratch directory and prove normal/TERM cleanup. Then investigate INT inheritance for asynchronous jobs; do not assume kill -INT is equivalent to Ctrl-C on a foreground process group.
2. `parallel.sh`: launch 3 `sleep` jobs, `wait` all, print each exit code; then version that `kill`s one mid-run and reports.
3. `quote-trap.sh`: double-quoted vs single-quoted trap bodies showing def-time vs fire-time expansion of the same variable.

## Related

- [[08-bash-functions-scope|Functions]] (`die`/cleanup helpers)
- [[09-bash-redirections|Redirections]]
- [[14-set-shopt-strict-debug|Set/Shopt/Strict Mode]] (`ERR/DEBUG`, `set -E/-T`)

Sources: [Bash signals](https://www.gnu.org/software/bash/manual/html_node/Signals.html), [job control builtins](https://www.gnu.org/software/bash/manual/html_node/Job-Control-Builtins.html). Gate: pass normal/TERM lifecycle checks and explain why cleanup cannot be guaranteed after SIGKILL.
