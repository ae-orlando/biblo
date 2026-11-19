#!/usr/bin/env bash
set -uo pipefail
if (( $# != 1 )); then printf 'usage: bash main.sh DIR\n' >&2; exit 2; fi
if [[ ! -d $1 || ! -r $1 || ! -x $1 ]]; then printf 'cannot read directory\n' >&2; exit 1; fi
find -- "$1" -mindepth 1 -maxdepth 1 -type f -printf '%f\0' | LC_ALL=C sort -z
