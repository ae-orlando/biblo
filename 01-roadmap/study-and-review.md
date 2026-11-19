# Study, review and assessment

## A useful session

1. State one observable outcome: “reject malformed inputs without changing the existing report,” not “study Bash.”
2. Predict one result before running code.
3. Read only the prerequisite section you need, then attempt the lab.
4. Interpret the first failing assertion. Distinguish an environment problem from a program defect.
5. Fix the cause and add or describe a regression case.
6. Explain the mechanism without copying the reference, then change a requirement.
7. Record a short evidence entry. Stop with a specific next action, not a fabricated green status.

Hints are allowed; record assistance honestly. Read a reference solution after an attempt or a deliberate study decision, then close it and rebuild a variant later.

## Completion rubric

| Dimension | Needs work | Independent evidence |
| --- | --- | --- |
| Correctness | Happy path only or unexplained output | Required cases pass; boundary cases are justified |
| Robustness | Invalid input corrupts state or hangs | Failure contract, bounded resources, cleanup and preserved invariants |
| Testing | Only syntax/lint or superficial assertions | A deliberate representative bug is caught |
| Design | Cannot explain choices | Defends a simpler alternative and a tradeoff |
| Security / safety | Host side effects, leaked data or unsafe assumptions | Appropriate permissions, local fixtures, no secret leakage |
| Transfer | Can only repeat the example | Meets a new requirement without following a solution |

Do not average away a critical safety or correctness failure with points elsewhere. Not every dimension applies to every tiny drill; all relevant dimensions apply to capstones.

## Lightweight spaced review

Suggested starting intervals: next study session, about a week later, then about three weeks later. Shorten an interval after a failed retrieval; lengthen it when the task is easy. These intervals are a convenient default, not a scientifically guaranteed schedule.

Review with one closed-note mechanism explanation and one small application or debugging task. Documentation remains allowed for the application. Mix an older topic into current work rather than rereading entire tracks.

Use `99-templates/review.md` or a plain checkbox with a date. No plugin is required. Review overdue items when useful; do not let a queue displace actual practice.

## Track checkpoint

Complete the track's cumulative task; save the artifact path, check result, manual evidence, bug caught, design explanation and changed requirement. Then choose “independent,” “with help,” “needs review,” or “not assessed.” An authored curriculum or passing reference suite is never learner evidence.
