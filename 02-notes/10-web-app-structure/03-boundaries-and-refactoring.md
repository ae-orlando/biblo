# Structure exercise — refactor without changing the contract

## Prerequisites and starting point

Complete api-dependencies or api-postgres yourself. Preserve the working attempt, then make a separate deliberate learner copy before refactoring. Do not overwrite supplied starters/references or someone else's work. See [[git-learning-path]] for preserving/reviewing your own changes.

## Task

1. Record actual passing checks and draw the current dependency/state/transaction boundaries.
2. Identify one source of coupling: HTTP-specific domain errors, hidden configuration, global state, duplicated parsing or persistence mixed into an unrelated helper.
3. Extract the smallest useful module/package boundary. Keep a thin app.py factory adapter so the existing lab checker can still load your attempt; a real packaged application can choose a different documented entry point.
4. Run the same behavioral checks. Do not rewrite tests merely to accept a regression caused by the move.
5. Add one new business requirement and explain whether the new boundary makes it easier to implement/test.

## Review questions

- Does domain code import FastAPI, a router or a CLI entry point unnecessarily?
- Is a connection owned/closed at the intended lifetime, with the whole invariant inside the intended transaction?
- Does importing the package start a server/read real secrets/change files?
- Can a test substitute an external boundary without mocking the actual business rule under test?
- Are request, response and persistence fields separated where their trust/meaning differ?
- Are modules named by responsibilities/features rather than miscellaneous utils dumped together?
- Did the refactor add unused abstraction or merely move complexity around?

## Evidence and completion

Save the before/after structure, passing checks, a dependency diagram, one caught defect and one tradeoff. Directory naming alone is not a behavioral test or a universal architecture grade. A flat structure can be the better choice for a small scope; explain that decision if it is your conclusion.

This is a learner/manual architecture exercise. It is not claimed completed by generating a tree or by the author's reference suites passing.
