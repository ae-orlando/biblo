---
created: 2026-10-08
updated: 2026-10-21
---


# Bash Basics (for Automation)

> This is an application bridge, not a second competing language course. Start with [[00-how-to-use-track]] when shell semantics are unfamiliar. Outcome: apply explicit argument/status contracts in `bash-cli`; then use [[30-script-workflow]] before host automation.

## Mental model

Script = list of commands the shell runs top to bottom. Verified here: `GNU bash 5.3.20`. Every command exits with a code: `0` = ok, else error (`$?` holds last). Quote everything that can contain spaces/globs. `"$@"` forwards args intact — bare `$@` does not.

Shebang + run:
```bash
#!/usr/bin/env bash
chmod +x run.sh
./run.sh a "b c"   # $1=a, $2="b c", $#=2, $@=all
```

## Core syntax

Variables (no spaces around `=`):
```bash
name="orlando"
pkg_count=3
echo "hi $name"        # double quotes expand, single don't: '$name' literal
default_port="${PORT:-8080}"   # :- fallback if unset/empty (safe under set -u)
: "${DATA_DIR:=$HOME/data}"    # := sets default if unset
```

Conditionals:
```bash
if [[ -f /etc/pacman.conf ]]; then
  echo "exists"
elif [[ "$1" == "--dry-run" ]]; then
  echo "would install"
else
  echo "other"
fi
# tests: -f file, -d dir, -L symlink, -x executable, -z empty, -n non-empty,
# == string, -eq/-ne/-lt numbers, && || inside [[ ]]
```

Loops:
```bash
for pkg in hyprland waybar kitty; do
  echo "install $pkg"
done

while IFS= read -r line; do
  echo "got: $line"
done < packages.txt   # IFS= + -r preserves spaces/backslashes
```

Functions (`local` only inside, dynamic scope):
```bash
install_pkg() {
  local pkg="$1"
  echo "installing $pkg"
  return 0   # return = function status; exit = kill whole script
}
install_pkg "hyprland"; echo $?
```

Arrays (the correct way to hold package lists):
```bash
pkgs=(hyprland waybar kitty "foo bar")
pkgs+=("new pkg")
printf '<%s>\n' "${pkgs[@]}"   # each element separate — CORRECT
# ${pkgs[*]} joins, $* splits+globs — WRONG for forwarding
echo "count: ${#pkgs[@]}"
mapfile -t lines < packages.txt  # file lines -> array, no splitting
```

## Arch note

`bash` is default shell. `$SHELL` here is `/usr/bin/zsh` — bash scripts still run via shebang `#!/usr/bin/env bash` regardless of interactive shell. Test snippets with `bash -c '...'` to isolate from zsh.

## Pitfalls

- `name = "x"` (spaces) tries to run command `name`.
- `echo $file` unquoted splits on spaces + expands `*` — always `"$file"` (SC2086).
- `local v=$(fail)` masks exit code (returns 0 even if `fail` errored) — split: `local v; v=$(fail)`.
- `cat file | grep x` works but wasteful — `grep x file` or `grep x < file` (SC2002, style).
- `if [ $? -ne 0 ]` after `cmd` — write `if ! cmd; then` directly (SC2181, avoids `$?` clobber + `set -e` exit).

## Try it

```bash
bash -c 'a="x y"; printf "<%s>\n" "$a" "$a"'
bash -c 'arr=("a b" "c*"); printf "<%s>\n" "${arr[@]}"; echo "n=${#arr[@]}"'
bash -c 'while IFS= read -r l; do echo "[$l]"; done <<< "a b
c*d"'
```

## Related

- [[10-robust-bash-scripts|Robust Scripts]]
- [[90-bash-protips|Bash Protips]]
- [[20-arch-automation|Arch Automation]]

Sources: [GNU Bash manual](https://www.gnu.org/software/bash/manual/), [ShellCheck wiki](https://www.shellcheck.net/wiki/). Practice and executed verification: [[practice-catalog]], [[implementation-status]]. Snippets are illustrative and not permission to alter packages or host configuration.
