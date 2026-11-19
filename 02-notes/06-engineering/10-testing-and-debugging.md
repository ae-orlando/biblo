# Testing and debugging — make claims falsifiable

## Outcome

Specify behavior, write a test that can fail for a real defect, and use observations to narrow a problem. Prerequisites: basic functions/exit status in your chosen track. Apply this note to every lab in [[practice-catalog]].

## A test is a contract, not a screenshot of output

Identify inputs, observable outputs/state, failure behavior and invariants. Cover representative valid, boundary, invalid and changed-data cases. Assert what matters, not implementation details unless those are explicitly the requirement. Sorting requirements need deliberate order assertions; unordered sets should not fail for harmless order differences.

Syntax checks parse. Linters detect selected patterns. Unit tests isolate a component; integration tests exercise boundaries; end-to-end/manual checks exercise the real workflow. Coverage counts executed code, not the quality of assertions. None alone establishes security or production readiness.

Example pattern (a scratch ESM test after implementing parseCount):

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseCount } from './main.mjs';
test('zero is valid, suffix junk is not', () => {
  assert.equal(parseCount('0'), 0);
  assert.throws(() => parseCount('42px'), RangeError);
});
```

Run the scratch test with `node --test YOUR-TEST.mjs`; use the launcher for bundled checks. First show a failure with an unfinished/incorrect implementation, then make it pass. If the “broken” version still passes, the suite has a gap.

## Isolate dependencies and control nondeterminism

Use fake data, temporary directories, explicit environment mappings, disposable databases and loopback ephemeral ports. Clean up only resources you own. Inject a clock or use controlled promises to test races; do not assert a fixed speedup or sleep until you hope a server is ready.

Negative tests must fail for the intended reason. Establish that the valid operation works before checking a rejected operation. A missing table is not proof that its UNIQUE constraint works. Mutation testing deliberately introduces a representative bug to test the tests; it is not equivalent to random vandalism.

## Debugging loop

1. Preserve the exact symptom, input, environment and relevant error/stack frames without secrets.
2. Classify syntax/runtime/logic/environment or integration failure.
3. Form one hypothesis, collect the smallest discriminating observation, then change one thing.
4. Reduce to a minimal reproducer when useful. Logs, assertions, breakpoints and tracing are complementary tools.
5. Fix the cause, add a regression case and check nearby behavior.

Practice: break quoting in `bash-quoting`, use parseInt in `js-values`, or COUNT(*) in `pg-queries`. Predict the failing check before running it. Record actual results, not just “fixed.”

## Completion

Explain one defect your suite missed and improve it. Distinguish a failing environment check from a learner implementation defect. Then meet a changed requirement without consulting a complete solution. See [[study-and-review]].

Sources: [Node test runner](https://nodejs.org/docs/latest-v24.x/api/test.html), [Python unittest](https://docs.python.org/3/library/unittest.html), [PostgreSQL regression testing concepts](https://www.postgresql.org/docs/18/regress.html).
