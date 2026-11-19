#!/usr/bin/env bash
set -euo pipefail
die() { printf '%s\n' "$1" >&2; exit 1; }
(( $# == 1 )) || die 'usage: bash main.sh MARKED_SANDBOX'
root=$1
[[ -d $root && ! -L $root && $root != / ]] || die 'unsafe sandbox'
[[ -f $root/.vault-permissions-lab && ! -L $root/.vault-permissions-lab ]] || die 'missing marker'
[[ $(< "$root/.vault-permissions-lab") == practice-only ]] || die 'wrong marker'
for name in public private bin; do
  [[ -d $root/$name && ! -L $root/$name ]] || die 'missing or symlinked directory'
done
for name in private/token bin/report.sh; do
  [[ -f $root/$name && ! -L $root/$name ]] || die 'missing or symlinked file'
done
chmod 755 -- "$root/public"
chmod 700 -- "$root/private"
chmod 750 -- "$root/bin" "$root/bin/report.sh"
chmod 600 -- "$root/private/token"
