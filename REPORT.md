# ECE444 PRA7 - Ali Alyaseri

November 19, 2026

**DRAFT - required screenshots still need to be inserted. All command output and GitHub results below come from saved execution/API records; they are transcripts and structured records, not terminal or browser screenshots. See evidence/CAPTURE_CHECKLIST.md before submitting.**

## 1. My fork and the practical

Ali Alyaseri | ECE444 PRA7 | November 19, 2026

I used the calculator to follow mistakes through manual linting, a local commit hook, and a pull request. The two starter tests passed during both lint-failure demonstrations. After recording the failures, I added regression tests for the behavior those tests had missed.

The supplied pyproject.toml is unchanged. Local Python and CI use 3.15.2; Ruff is pinned to 0.17.4, pre-commit to 4.7.0, and pytest to 9.2.0.

[My fork](https://github.com/AliAlya/ECE444-PRA7)

[Demonstration and repair: PR #1](https://github.com/AliAlya/ECE444-PRA7/pull/1)

## 2. The three initial lint findings

I replaced calculator.py with the supplied flawed sample. Ruff found F401 (unused import), F841 (unused variable), and B006 (mutable default argument). The original two addition tests still passed because they did not exercise record or inspect unused names.

This shows the limit of the original tests: checking two addition results does not establish that every function is free of problems.

### Initial lint output (saved command transcript)

```text
> .venv/Scripts/python.exe -m ruff check calculator.py

F401 [*] `os` imported but unused
 --> calculator.py:1:8
  |
1 | import os
  |        ^^
help: Remove unused import: `os`
  |
  - import os
1 |
  |

F841 Local variable `unused` is assigned to but never used
 --> calculator.py:5:5
  |
4 | def add(a,b):
5 |     unused = 123
  |     ^^^^^^
6 |     return a + b
  |
help: Remove assignment to unused variable `unused`
  |
4 | def add(a,b):
  -     unused = 123
5 |     return a + b
  |
note: This is an unsafe fix and may change runtime behavior

B006 Do not use mutable data structures for argument defaults
  --> calculator.py:9:27
   |
 9 | def record(value, history=[]):
   |                           ^^
10 |     history.append(value)
11 |     return history
   |
help: Replace with `None`; initialize within function
   |
8  |
   - def record(value, history=[]):
9  + def record(value, history=None):
10 +     if history is None:
11 +         history = []
12 |     history.append(value)
   |
note: This is an unsafe fix and may change runtime behavior

Found 3 errors.
[*] 1 fixable with `--fix` (2 unsafe fixes available with `--fix --unsafe-fixes`).

Exit code: 1
```

[Source record](evidence/logs/04-item2-lint-before.json)

[Additional source: 05-item2-tests-still-pass.json](evidence/logs/05-item2-tests-still-pass.json)

**Required screenshot pending:** `evidence/screenshots/item02-lint-before.png`.

## 3. What the safe automatic fix changed

I ran Ruff with --fix. It removed the unused os import, leaving F841 and B006. The command exited with code 1 because those findings were still unresolved.

I reviewed the remaining code instead of turning on unsafe fixes or suppressing the checks. Removing an arbitrary assignment can remove side effects; changing a default argument can change behavior. Those repairs need an understanding of the function.

### Safe fix output (saved command transcript)

```text
> .venv/Scripts/python.exe -m ruff check --fix calculator.py

F841 Local variable `unused` is assigned to but never used
 --> calculator.py:4:5
  |
3 | def add(a,b):
4 |     unused = 123
  |     ^^^^^^
5 |     return a + b
  |
help: Remove assignment to unused variable `unused`
  |
3 | def add(a,b):
  -     unused = 123
4 |     return a + b
  |
note: This is an unsafe fix and may change runtime behavior

B006 Do not use mutable data structures for argument defaults
  --> calculator.py:8:27
   |
 8 | def record(value, history=[]):
   |                           ^^
 9 |     history.append(value)
10 |     return history
   |
help: Replace with `None`; initialize within function
   |
7  |
   - def record(value, history=[]):
8  + def record(value, history=None):
9  +     if history is None:
10 +         history = []
11 |     history.append(value)
   |
note: This is an unsafe fix and may change runtime behavior

Found 3 errors (1 fixed, 2 remaining).
2 unsafe fixes available with `--fix --unsafe-fixes`.

Exit code: 1
```

[Source record](evidence/logs/06-item3-safe-fix.json)

**Required screenshot pending:** `evidence/screenshots/item03-safe-fix.png`.

## 4. My manual repair and formatting check

I removed unused = 123 and changed history=[] to history=None, creating a new list only when history is None. This keeps unrelated calls separate while preserving a list intentionally passed by the caller.

I used is None rather than a truthiness check so an explicitly supplied empty history list is still updated. Ruff then passed. I also applied the handout's poorly spaced add function and confirmed the formatter reported one file reformatted.

### Repaired calculator at this stage

```python
def add(a, b):
    return a + b


def record(value, history=None):
    if history is None:
        history = []
    history.append(value)
    return history
```

### Passing lint output (saved command transcript)

```text
> .venv/Scripts/python.exe -m ruff check calculator.py

All checks passed!

Exit code: 0
```

[Source record](evidence/logs/07-item4-repaired.json)

### Formatting demonstration (saved command transcript)

```text
> .venv/Scripts/python.exe -m ruff format calculator.py

1 file reformatted

Exit code: 0
```

[Source record](evidence/logs/09-formatting-demo.json)

**Required screenshot pending:** `evidence/screenshots/item04-repaired.png`.

## 5. My additional violation: B015

I added add_to_total(total, value), but used total == add(total, value). That expression compares values and discards the Boolean result. It never updates total. Ruff reported B015, and add_to_total(12, 8) returned 12 instead of 20.

I changed == to =. The same call then returned 20 and Ruff passed. An assertion would not match the function's purpose; this operation needs to update the running total.

### Before

```python
def add_to_total(total, value):
    total == add(total, value)
    return total
```

### After

```python
def add_to_total(total, value):
    total = add(total, value)
    return total
```

### Before: B015 (saved command transcript)

```text
> .venv/Scripts/python.exe -m ruff check calculator.py

B015 Pointless comparison. Did you mean to assign a value? Otherwise, prepend `assert` or remove it.
  --> calculator.py:13:5
   |
12 | def add_to_total(total, value):
13 |     total == add(total, value)
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^
14 |     return total
   |

Found 1 error.

Exit code: 1
```

[Source record](evidence/logs/10-item5-b015-before.json)

### After: lint passes (saved command transcript)

```text
> .venv/Scripts/python.exe -m ruff check calculator.py

All checks passed!

Exit code: 0
```

[Source record](evidence/logs/12-item5-b015-after.json)

[Additional source: 11-item5-wrong-result.json](evidence/logs/11-item5-wrong-result.json)

[Additional source: 13-item5-correct-result.json](evidence/logs/13-item5-correct-result.json)

**Required screenshot pending:** `evidence/screenshots/item05-before.png`.

**Required screenshot pending:** `evidence/screenshots/item05-after.png`.

## 6. The working GitHub Actions baseline

I copied the supplied CI template and replaced its three TODO commands. The lint job runs Ruff with GitHub annotations, the format job uses --check, and the tests job runs pytest with --maxfail=1. The remaining workflow settings are unchanged.

Each job checks out the repository, configures Python, and installs dependencies independently because jobs run on separate machines. The baseline run completed with all three jobs successful.

[Specific passing baseline run](https://github.com/AliAlya/ECE444-PRA7/actions/runs/44465783555)

| Job | Conclusion | Completed (UTC) |
| --- | --- | --- |
| format | success | 2026-11-19T05:32:19Z |
| lint | success | 2026-11-19T05:32:17Z |
| tests | success | 2026-11-19T05:32:18Z |

**Required screenshot pending:** `evidence/screenshots/item06-baseline-ci.png`.

## 7. F821 and the rejected commit

On demonstrate-ruff, I appended the required broken_total function. missing_total is undefined. Ruff caught F821 at calculator.py:18:12, while the original two addition tests passed. Merely importing the function does not execute its body.

A normal commit was rejected by ruff-check; ruff-format passed. For the subsequent demonstration commit only, I set SKIP to ruff-check, left formatting active, and cleared SKIP immediately afterward. This let CI independently inspect the same defect.

### Deliberate defect

```python
def broken_total():
    return missing_total
```

### Manual lint failure (saved command transcript)

```text
> .venv/Scripts/python.exe -m ruff check .

F821 Undefined name `missing_total`
  --> calculator.py:18:12
   |
17 | def broken_total():
18 |     return missing_total
   |            ^^^^^^^^^^^^^

Found 1 error.

Exit code: 1
```

[Source record](evidence/logs/20-item7-f821.json)

### Starter tests (saved command transcript)

```text
> .venv/Scripts/python.exe -m pytest -q

..                                                                       [100%]
2 passed in 0.01s

Exit code: 0
```

[Source record](evidence/logs/21-item7-tests.json)

### Normal commit rejected (saved command transcript)

```text
> git commit -m "Show that the hook catches an undefined total"

ruff check...............................................................Failed
- hook id: ruff-check
- exit code: 1

F821 Undefined name `missing_total`
  --> calculator.py:18:12
   |
17 | def broken_total():
18 |     return missing_total
   |            ^^^^^^^^^^^^^

Found 1 error.

ruff format..............................................................Passed

Exit code: 1
```

[Source record](evidence/logs/22-item7-rejected-commit.json)

[Additional source: 23-demonstration-skip.json](evidence/logs/23-demonstration-skip.json)

**Required screenshot pending:** `evidence/screenshots/item07-code.png`.

**Required screenshot pending:** `evidence/screenshots/item07-f821-tests.png`.

**Required screenshot pending:** `evidence/screenshots/item07-rejected-commit.png`.

## 8. Requiring successful checks on main

I saved require-ci-on-main on my own fork after the baseline workflow ran. The ruleset is active, targets the default branch (main), requires a pull request, and requires lint, format, and tests. Required approvals are zero for this individual exercise.

The bypass list is empty. Requiring the branch to be up to date is disabled, and checks are enforced on creation. The active-rules endpoint confirmed the rules apply to main. During the intentional failure, GitHub reported the PR merge state as BLOCKED.

[Saved ruleset](https://github.com/AliAlya/ECE444-PRA7/rules/27612614)

| Setting | Saved value |
| --- | --- |
| Name | require-ci-on-main |
| Enforcement | active |
| Target | Default branch: main |
| Bypass actors | [] |
| Pull request | Required; approvals: 0 |
| Required checks | lint, format, tests |
| Require up-to-date branch | No |
| Skip checks on creation | No |

[Additional source: 17-ruleset-saved.json](evidence/logs/17-ruleset-saved.json)

[Additional source: 24-main-active-rules.json](evidence/logs/24-main-active-rules.json)

**Required screenshot pending:** `evidence/screenshots/item08-ruleset.png`.

## 9. CI catches the failing pull request

I opened PR #1 from demonstrate-ruff into my own fork's main. At commit 95a963e, lint failed, format passed, and tests passed. The saved PR record shows BLOCKED, so the failed required check prevented merging.

The failed job's expanded Ruff log identifies the exact undefined name and file/line reference. The historical run and job remain inspectable after the repair.

[Same pull request](https://github.com/AliAlya/ECE444-PRA7/pull/1)

[Historical failed CI run](https://github.com/AliAlya/ECE444-PRA7/actions/runs/44466075166)

[F821 lint job](https://github.com/AliAlya/ECE444-PRA7/actions/runs/44466075166/job/135364052312)

| Job | Conclusion | Completed (UTC) |
| --- | --- | --- |
| lint | failure | 2026-11-19T05:34:40Z |
| tests | success | 2026-11-19T05:34:29Z |
| format | success | 2026-11-19T05:34:30Z |

```text
﻿2026-11-19T05:34:37.6322754Z ##[group]Run python -m ruff check --output-format=github .
2026-11-19T05:34:37.6609483Z ##[error]calculator.py:18:12: F821 Undefined name `missing_total`
2026-11-19T05:34:37.6616235Z ##[error]Process completed with exit code 1.
```

[Additional source: 25-item9-failing-pr.json](evidence/logs/25-item9-failing-pr.json)

[Additional source: 27-item9-f821-job.txt](evidence/logs/27-item9-f821-job.txt)

**Required screenshot pending:** `evidence/screenshots/item09-failed-summary.png`.

**Required screenshot pending:** `evidence/screenshots/item09-f821-log.png`.

## 10. Repairing the same PR

I repaired broken_total to return add_to_total(12, 8), which evaluates to 20, then pushed to the same demonstrate-ruff branch. Both local hooks ran normally. The repaired run has successful lint, format, and tests jobs; the same PR became CLEAN.

After capturing the two-test failure demonstration, I added four regression tests: independent default histories, preservation of a supplied empty history list, updating an existing total, and calling the repaired function. The final suite has six passing tests.

I left PR #1 open for TA review. The handout requires a repaired passing PR and does not explicitly require merging it. Quercus upload and the oral explanation remain personal submission steps.

[Repaired PR](https://github.com/AliAlya/ECE444-PRA7/pull/1)

[Specific repaired CI run](https://github.com/AliAlya/ECE444-PRA7/actions/runs/44466570039)

| Job | Conclusion | Completed (UTC) |
| --- | --- | --- |
| lint | success | 2026-11-19T05:38:58Z |
| format | success | 2026-11-19T05:38:50Z |
| tests | success | 2026-11-19T05:39:06Z |

### Final local tests (saved command transcript)

```text
> .venv/Scripts/python.exe -m pytest -q

......                                                                   [100%]
6 passed in 0.03s

Exit code: 0
```

[Source record](evidence/logs/31-repair-tests.json)

[Additional source: 29-repair-lint.json](evidence/logs/29-repair-lint.json)

[Additional source: 30-repair-format-check.json](evidence/logs/30-repair-format-check.json)

[Additional source: 34-item10-repaired-pr.json](evidence/logs/34-item10-repaired-pr.json)

**Required screenshot pending:** `evidence/screenshots/item10-repaired-pr.png`.
