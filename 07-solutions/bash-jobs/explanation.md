# Reference: cleanup is explicit ownership

The reference records child PIDs immediately, chooses signal exit statuses, then uses one EXIT handler to terminate/reap children and remove its empty directory. It saves and restores the original status. EXIT does not run after SIGKILL, and signal inheritance differs for background jobs.

The checker isolates its own process group and never trusts arbitrary reported PIDs for cleanup. Verification: `python3 90-tools/practice.py check bash-jobs --reference`.
