# Reference: ordering is not timing

`latestOnly` numbers calls within a closure and checks that number after settlement. It suppresses obsolete results but does not cancel work. The mapper uses a bounded set of consumers and stores results by input index; `Promise.all` observes every consumer's rejection.

Failure stops future scheduling when observed; tasks already started may still have effects. For effectful work, decide cancellation, rollback and retry policy explicitly. Mutation to catch: returning results in completion order or sharing a global latest counter. Verification: `python3 90-tools/practice.py check js-async --reference`.
