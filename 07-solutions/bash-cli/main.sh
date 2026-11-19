#!/usr/bin/env bash
set -euo pipefail
usage() { printf 'usage: bash main.sh [--dry-run] --output FILE [--] INPUT\n'; }
die() { printf '%s\n' "$1" >&2; exit "${2:-1}"; }
dry=0; output=''; positional=()
while (( $# )); do
  case $1 in
    --help) usage; exit 0 ;;
    --dry-run) dry=1; shift ;;
    --output) (( $# >= 2 )) || die 'usage: --output requires a value' 2; output=$2; shift 2 ;;
    --) shift; positional+=("$@"); break ;;
    -*) die 'usage: unknown option; use -- before a dash-leading input' 2 ;;
    *) positional+=("$1"); shift ;;
  esac
done
[[ -n $output && ${#positional[@]} == 1 ]] || die 'usage: one input and --output are required' 2
input=${positional[0]}
[[ -f $input && -r $input ]] || die 'input is not a readable regular file'
[[ ! -L $output ]] || die 'refusing symlink output'
[[ ! -e $output || -f $output ]] || die 'output is not a regular file'
[[ $input != "$output" && ! $input -ef $output ]] || die 'input and output must differ'
parent=$(dirname -- "$output")
[[ -d $parent && -w $parent ]] || die 'output parent must exist and be writable'
if (( dry )); then printf 'Would number %q into %q\n' "$input" "$output"; exit 0; fi
temp=''
cleanup() { [[ -z $temp ]] || rm -f -- "$temp"; }
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
temp=$(mktemp -- "$parent/.vault-report.XXXXXX")
line_number=0
while IFS= read -r line || [[ -n $line ]]; do
  line_number=$((line_number + 1))
  printf '%s\t%s\n' "$line_number" "$line"
done < "$input" > "$temp"
mv -f -- "$temp" "$output"
temp=''
