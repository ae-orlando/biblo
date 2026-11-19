# Git 04 — remotes, integration and review

## Outcome

Distinguish local history from remote references and make review about behavior, not only formatting. Prerequisite: branches/merges. The first exercise is local; no hosting account, remote or publication is needed.

origin is a conventional remote name, not a special trusted server. A remote-tracking reference records your last fetched knowledge of a remote ref, not a live view of its current state. fetch normally updates fetched objects/references without integrating them into your current working branch. pull combines fetching with a configured/chosen integration strategy; it is not always “just merge.”

push proposes updates to selected remote references. It can publish private content/history; a private/local working tree is not safe to push merely because its latest diff contains no secret. Inspect what history and refs will be shared and who can access the destination.

## Review a meaningful change

- What problem/contract is being changed? Are compatibility and failure behavior explicit?
- Do implementation and schema changes preserve invariants/authorization?
- Are tests capable of detecting the relevant defect, including invalid and unauthorized cases?
- Does setup/configuration/documentation match actual source and runtime?
- Are secrets, runtime artifacts or unrelated changes included?
- Which tradeoff or unresolved risk deserves discussion rather than a cosmetic nit?

A pull request is a collaboration/review workflow supplied by a hosting tool, not a Git commit type. You can practise review locally by comparing branches and writing a structured review. Do not fabricate another person's approval or a published PR as evidence.

## Later optional exercise

After choosing a remote deliberately, inspect its URL/upstream mapping and explain fetch/integration/push before performing them. Remote URLs/logs may contain private account information or badly embedded credentials; sanitize evidence. No force-push, remote modification or account sign-in is performed automatically by these notes/tools.

Sources: [remotes](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes), [git fetch](https://git-scm.com/docs/git-fetch), [git pull](https://git-scm.com/docs/git-pull), [git push](https://git-scm.com/docs/git-push).
