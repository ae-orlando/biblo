# Python 10 — tests, types and maintainable boundaries

## Outcome

Make behavior falsifiable, distinguish static guidance from runtime validation, and diagnose a failed assertion. Prerequisites: functions/errors. Apply this throughout Python; revisit before py-design/py-cli.

The supplied checks use standard-library unittest, so beginning does not require learning/installing a separate test framework. A TestCase groups cases; assertions compare observed behavior with a stated contract. pytest is a common later alternative, not a prerequisite to understanding why a test is meaningful.

```python
import unittest

class ArithmeticTests(unittest.TestCase):
    def test_example(self):
        self.assertEqual(2 + 3, 5)
```

This tiny syntax example is not a useful test of your application. Replace the expression with a call to your own function and choose a case that distinguishes a correct implementation from a plausible bug. Use assertRaises for intended failure types and check state after rejection.

## What tests establish

Test valid behavior first, then boundaries, malformed input, unchanged state and independent repeated calls. Fixtures should be deterministic and owned by the test. A rejected missing table is not proof of a working constraint; a malformed response is not automatically a network timeout.

Unit tests target a small component; integration tests exercise a real boundary such as a process, parser or database. Manual/browser testing covers behaviors a unit test cannot observe. A syntax check or high coverage percentage is not mastery/security evidence.

## Types are another feedback channel

Annotations such as def parse(text: str) -> int describe intent to readers and static tools. Python does not automatically enforce them at every call. Validate untrusted external inputs explicitly. A type checker can catch some mismatches but not whether a shipping threshold matches the business rule.

Keep domain calculations independent of print/input/files where practical. Pass dependencies such as configuration or gateways in so tests can substitute controlled values. Do not mock the very behavior you are trying to establish—for database concurrency, use a real disposable database test.

## Practice gate

Introduce one bug in a private copy: change a threshold, accept boolean money, share instance state, or truncate a report before serialization. Predict the failing test and show it fails. Then add a previously missing requirement and a regression case of your own. Use [[10-testing-and-debugging]] and [[study-and-review]] to record assistance/limits honestly.

Sources: [unittest](https://docs.python.org/3.14/library/unittest.html), [typing](https://docs.python.org/3.14/library/typing.html).
