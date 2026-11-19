# Reporting CLI — progressive hints

1. Parse CLI arguments separately from loading, calculation and output. argparse can provide the help/usage boundary.
2. Reuse your own format/record knowledge; aggregate category count/cents without hidden global state.
3. Do not print success or replace output until validation succeeds. Dry-run returns before output staging, and expected errors translate to status 1 without a fake successful report.
