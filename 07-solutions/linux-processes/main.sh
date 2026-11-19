#!/usr/bin/env bash
set -euo pipefail
if (( $# != 1 )) || [[ ! $1 =~ ^[1-9][0-9]*$ ]]; then
  printf 'usage: bash main.sh POSITIVE_PID\n' >&2; exit 2
fi
file=/proc/$1/status
if [[ ! -r $file ]]; then printf 'process missing or inaccessible\n' >&2; exit 1; fi
awk -F '\t' '$1 == "Name:" || $1 == "Pid:" || $1 == "PPid:" { sub(/:$/, "", $1); printf "%s\t%s\n", $1, $2 }' < "$file"
