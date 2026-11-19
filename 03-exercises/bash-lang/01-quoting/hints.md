# Filename lab — progressive hints

1. A filename can contain a newline but cannot contain NUL. Preserve records with NUL all the way through.
2. Quote the directory argument; use an explicit option terminator where the tool supports it. Decide file type and traversal depth in `find`.
3. GNU `find -printf` can emit a basename and NUL directly; GNU `sort -z` sorts NUL-delimited records. This is a GNU/Linux contract, not a POSIX portability claim.
