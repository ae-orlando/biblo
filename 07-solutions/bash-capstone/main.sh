#!/usr/bin/env bash
# Bash 5+, GNU find/stat/sort. Not compatible with macOS's default Bash 3.2.
set -euo pipefail
export LC_ALL=C
die() { printf '%s\n' "$1" >&2; exit "${2:-1}"; }
top=10; dry=0; args=()
while (( $# )); do
  case $1 in
    --help) printf 'usage: bash main.sh [--dry-run] [--top N] [--] DIR\n'; exit 0 ;;
    --dry-run) dry=1; shift ;;
    --top) (( $# >= 2 )) || die 'missing --top value' 2; top=$2; shift 2 ;;
    --) shift; args+=("$@"); break ;;
    -*) die 'unknown option' 2 ;;
    *) args+=("$1"); shift ;;
  esac
done
[[ ${#args[@]} == 1 && $top =~ ^[1-9][0-9]{0,5}$ ]] || die 'usage: one DIR; --top must be 1..999999' 2
dir=${args[0]}
[[ -d $dir && -r $dir && -x $dir ]] || die 'directory is not readable'
if (( dry )); then printf 'Would inventory %q (read-only)\n' "$dir"; exit 0; fi
declare -A counts=() sizes=()
mapfile -d '' -t files < <(find -- "$dir" -type f -print0)
finder=$!
wait "$finder" || die 'directory traversal failed'
for file in "${files[@]}"; do
  base=${file##*/}; extension=none
  if [[ $base != .* && $base == *.* ]]; then
    extension=${base##*.}; extension=${extension,,}
    [[ $extension =~ ^[a-z0-9]+$ ]] || extension=other
  fi
  bytes=$(stat -c '%s' -- "$file")
  counts[$extension]=$(( ${counts[$extension]:-0} + 1 ))
  sizes[$extension]=$(( ${sizes[$extension]:-0} + bytes ))
done
printf 'extension,count,bytes\n'
if (( ${#counts[@]} )); then
  # sed reads the whole stream, unlike head: avoid a SIGPIPE/pipefail surprise.
  for extension in "${!counts[@]}"; do
    printf '%s,%s,%s\n' "$extension" "${counts[$extension]}" "${sizes[$extension]}"
  done | sort -t, -k2,2nr -k1,1 | sed -n "1,${top}p"
fi
