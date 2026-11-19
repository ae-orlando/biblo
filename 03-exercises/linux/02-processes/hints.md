# Process inspection — progressive hints

1. Validate the complete numeric argument before constructing a /proc path.
2. `/proc/PID/status` is structured text; field labels are not the same as line positions.
3. Match the exact Name/Pid/PPid labels and preserve values after the tab. No eval, sudo or signal is needed. A real diagnostic should distinguish observations from conclusions.
