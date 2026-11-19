#!/usr/bin/env bash
set -euo pipefail
if (( $# != 1 )) || [[ ! -d $1 ]]; then printf 'usage: bash main.sh WORKDIR\n' >&2; exit 2; fi
temp=''; children=()
cleanup() {
  local status=$?
  trap - EXIT
  local pid
  for pid in "${children[@]}"; do kill -TERM "$pid" 2>/dev/null || :; done
  for pid in "${children[@]}"; do wait "$pid" 2>/dev/null || :; done
  [[ -z $temp ]] || rmdir -- "$temp"
  exit "$status"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
temp=$(mktemp -d -- "$1/worker.XXXXXX")
sleep 60 & children+=("$!")
sleep 60 & children+=("$!")
printf 'READY\t%s\t%s\t%s\n' "$temp" "${children[0]}" "${children[1]}"
IFS= read -r action || exit 1
[[ $action == 'done' ]] || exit 2
