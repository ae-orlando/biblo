# Python 01 — run instructions and call a function

## Outcome and starting point

Distinguish the terminal, interpreter, source file, function definition and function call. No previous Python is assumed. Practice: `py-basics` in [[practice-catalog]].

A program is stored instructions and data. A .py file contains Python text; the interpreter reads/parses it and executes its top-level statements. The terminal runs commands such as python3; it is not itself a Python interpreter.

```bash
python3 --version
python3 -c 'print("Hello, learner")'
```

The outer quotes belong to your shell; the text inside is Python. Run python3 without -c to open its interactive prompt. Type Python after the prompt, not the displayed >>> characters. Exit with exit() or the terminal's EOF convention.

## The smallest function model

```python
def double(number):
    return number * 2

answer = double(7)
print(answer)  # 14
```

def creates a reusable function named double. number is its input name. The colon starts an indented body; use four spaces consistently. A definition does not execute the body. double(7) calls it with 7. return sends a value back to the caller; print displays text but is not a substitute for returning the value the caller needs.

An assignment stores a reference under a name. = is assignment; == compares. Comments begin with # outside strings. A syntax error means the source could not be parsed; another error can occur after execution starts. Read the error and relevant filename/line, not only the final red text.

## First actual attempt

Start py-basics from [[python-learning-path]], open its work/main.py, and read the supplied function signature. The NotImplementedError is a temporary marker that intentionally fails when the checker calls your function; replace that line with your calculation. You do not need to master exceptions first.

Running a file containing only a definition may display nothing. That is expected: no call printed a result. The lab's checker imports the file, calls the function and asserts the returned value for several inputs.

## Retrieval and extension

Before running, predict the value of answer and what prints. Explain why print(double(7)) differs from defining double. Change the caller's input and verify the result without editing the function for each example. A function that returns one hard-coded fixture answer has not learned the rule.

Next: [[02-python-values]]. Source: [interpreter use](https://docs.python.org/3.14/tutorial/interpreter.html), [functions](https://docs.python.org/3.14/tutorial/controlflow.html#defining-functions).
