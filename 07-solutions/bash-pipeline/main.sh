#!/usr/bin/env bash
set -uo pipefail
if (( $# != 1 )); then printf 'usage: bash main.sh LOG\n' >&2; exit 2; fi
if [[ ! -f $1 || ! -r $1 ]]; then printf 'cannot read log\n' >&2; exit 1; fi
awk -F '\t' '
  !($1 == "INFO" || $1 == "WARN" || $1 == "ERROR") || NF < 2 || $2 == "" {
    printf "invalid log record at line %d\n", NR > "/dev/stderr"; bad=1; next
  }
  { counts[$1]++ }
  END {
    if (bad) exit 1
    printf "ERROR\t%d\nINFO\t%d\nWARN\t%d\n", counts["ERROR"], counts["INFO"], counts["WARN"]
  }
' < "$1"
