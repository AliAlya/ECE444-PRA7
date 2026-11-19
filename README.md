# ECE444 PRA7 - Catching mistakes before they get merged

Ali Alyaseri | [AliAlya/ECE444-PRA7](https://github.com/AliAlya/ECE444-PRA7)

This practical uses a small calculator to follow a mistake through a manual Ruff check, a local Git hook, and a GitHub pull request. The interesting result is that the original two tests can pass while Ruff still identifies a problem. Each check sees a different part of the code.

Based on the [PRA7 handout](https://shuruizuoft.github.io/ECE444-Fall2026/pras/static-analysis-ci.html) and forked from the [course starter](https://github.com/shuruizUofT/ece444-pra7-starter). The supplied Ruff configuration and tool versions are preserved.

## Verified result

| Stage | Result and evidence |
| --- | --- |
| Working baseline | All three jobs passed: [baseline run](https://github.com/AliAlya/ECE444-PRA7/actions/runs/44465783555). |
| Intentional defect | F821 failed lint; formatting and the two starter tests passed: [failed run](https://github.com/AliAlya/ECE444-PRA7/actions/runs/44466075166). GitHub reported the PR merge state as `BLOCKED`. |
| Repair | All three jobs passed: [repaired run](https://github.com/AliAlya/ECE444-PRA7/actions/runs/44466570039). The same PR became `CLEAN`. |
| Branch protection | [require-ci-on-main](https://github.com/AliAlya/ECE444-PRA7/rules/27612614) is active; its bypass list is empty and all three checks are required. |
| Pull request | [PR #1](https://github.com/AliAlya/ECE444-PRA7/pull/1), from my `demonstrate-ruff` branch into my own fork's `main`. Left open so the TA can review the demonstration and repaired checks together. |
| Local final code | Ruff lint and formatting pass. **6 tests pass**, including four regression tests added after the failure demonstration. |

**Submission status:** the code and GitHub demonstration are complete. The [numbered report](REPORT.md) and generated PDF preserve real command transcripts and GitHub API records. Required terminal/browser screenshots still need to be inserted; browser automation stopped because it could not reliably establish the current URL. The PDF is marked as a draft until those images are supplied. [Capture checklist](evidence/CAPTURE_CHECKLIST.md).

## Activities and what I did

| Activity | Work and purpose |
| --- | --- |
| Prepare the fork | Forked the starter into my own account and created a Python 3.15.2 environment. |
| Configure Ruff | Copied `pyproject.toml` unchanged. It enables E, F, I, and B rules, with E501 ignored as supplied. Ran the starter tests, lint, and formatting checks. |
| Install pre-commit | Installed `ruff-check` and `ruff-format`. The lint hook applies safe fixes and exits nonzero after modifying a file so I can review and stage it. |
| Investigate findings | Loaded the flawed calculator, recorded F401/F841/B006, ran the safe fixer, then manually repaired the remaining findings. |
| Format code | Formatted the handout's poorly spaced `add` function. The layout changed; the calculation stayed the same. |
| Try another rule | Created B015 in a running-total example. Recorded the incorrect result, fixed it, and checked the corrected result. |
| Add CI | Copied the supplied workflow and filled its three TODO commands. Lint, formatting, and tests run as independent jobs. |
| Demonstrate failure | Used `demonstrate-ruff` and `broken_total` to show F821 locally, a rejected commit, and a failing PR check. |
| Require checks and repair | Require `lint`, `format`, and `tests` before merging into my fork's main branch, then repair the same PR. The report records the observed GitHub results. |

## The repairs I should be able to explain

### F401: an unused import

The sample imports `os` but never uses it. `ruff check --fix` removes that import. The command still exits with a failure because F841 and B006 remain.

### F841: an assigned value that is never read

`unused = 123` has no role in `add`, so I removed it. Ruff classifies the general automatic fix as unsafe because removing an assignment could also remove an expression with side effects. Here the right-hand side is a literal, so the manual repair is straightforward.

### B006: history leaking between calls

Python evaluates a default argument when the function is defined. With `history=[]`, calls that omit `history` share the same list. Recording one value can affect a later independent call.

```python
def record(value, history=None):
    if history is None:
        history = []
    history.append(value)
    return history
```

Each omitted history now creates a fresh list. A caller that explicitly supplies an existing list still gets that list extended. I used `is None` rather than `if not history` because an intentionally supplied empty list is valid too.

### My additional rule: B015, a discarded comparison

I chose a mistake that could happen while extending the calculator:

```python
def add_to_total(total, value):
    total == add(total, value)
    return total
```

`==` compares two values and produces a Boolean. This function discards that Boolean, so `add_to_total(12, 8)` returns **12** although the expected total is **20**. Ruff reports B015. The repair is an assignment:

```python
def add_to_total(total, value):
    total = add(total, value)
    return total
```

The same input then returns **20**, and Ruff passes. I kept the intermediate assignment so the change from comparison to assignment stays easy to see in the evidence.

### F821: a name that does not exist

The deliberate PR defect is:

```python
def broken_total():
    return missing_total
```

Importing this function does not execute its body. The starter tests call `add`, so they pass without reaching `missing_total`. Ruff inspects the source and reports F821 without needing a test to call the function. Calling the defective function would raise `NameError`.

## What the final tests cover

The original two tests check positive and negative addition. I left those tests unchanged during the failure demonstration, so the report genuinely shows **2 passing tests alongside F821**. After recording that result, I added four regression tests:

- Two independent `record` calls must get separate lists. This catches the original B006 behavior.
- An explicitly supplied empty list must be the same object returned and updated. This catches an incorrect `if not history` repair.
- Adding 8 to an existing total of 12 must return 20. This catches the B015 mistake.
- Calling the repaired `broken_total` must return 20. The old version would raise `NameError`.

The repaired `broken_total` calls `add_to_total(12, 8)`. Its name remains the one required by the handout so the before/after history is easy to follow. The final suite has **6 tests**; the extra four were added after the intentional failure was captured.

## Files I should know

| File | Purpose |
| --- | --- |
| `calculator.py` | Addition, recording history, updating a total, and the repaired demonstration function. |
| `test_calculator.py` | Original addition tests and the four regression tests described above. |
| `pyproject.toml` | Shared Ruff rules, target Python version, and formatting settings. |
| `.pre-commit-config.yaml` | Pinned Ruff lint/fix and formatting hooks. |
| `.github/workflows/ci.yml` | Three separate GitHub Actions jobs, triggered by pushes to main and pull requests. |
| `requirements-dev.txt` | Exact assignment versions of Ruff, pre-commit, and pytest. |
| `lab-assets/` | Original templates and flawed sample, kept for reference. |
| `evidence/logs/` | Saved command outputs, source snapshots, and GitHub records for the report. |
| `REPORT.md` | The ten numbered report items and evidence links. |
| `tools/build_report.py` | Rebuilds the local PDF, including any supplied screenshots. |
| `tools/replay_evidence.py` | Reruns local evidence stages in separate scratch folders for screenshots, without changing or pushing the completed work. |

## Run it on my Windows computer

From the PRA7 folder, use the environment's executable directly. Activation and PowerShell execution-policy changes are unnecessary.

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m pre_commit run --all-files
```

Python is **3.15.2**, Ruff **0.17.4**, pre-commit **4.7.0**, and pytest **9.2.0**. A project-local copy of official Python is in `.tools/python315`; it is ignored by Git. The machine's general `python` command points to a different installation, so the explicit `.venv` path avoids ambiguity.

To recreate the environment on this computer while `.tools/python315` is present:

```powershell
.\.tools\python315\python.exe -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pre_commit install
```

On another computer with Python 3.15 installed, use `py -3.15 -m venv .venv` for the first line. Hooks must be installed in each clone; committing the configuration does not install someone else's Git hook.

To apply formatting while editing:

```powershell
.\.venv\Scripts\python.exe -m ruff format .
```

If a hook modifies a file, review the diff, stage it again, and retry the commit.

## How the checks fit together

Manual checks, hooks, and CI all read `pyproject.toml`. The dependency file and hook configuration pin matching Ruff versions. Pre-commit creates its own cached environment, so the installed hook works even without activating my `.venv`.

Each CI job gets a fresh runner, checks out the code, sets up Python, and installs dependencies. Lint can fail while formatting and tests still report their own results. `--output-format=github` produces lint annotations. `ruff format --check` reports formatting differences without rewriting the code.

A failed job reports a problem. The active `require-ci-on-main` ruleset makes passing checks a condition for merging. It targets the default branch, requires a PR and all three checks, requires zero approvals for this individual exercise, and has no bypass actors.

For the deliberate failure, I skipped only `ruff-check` for one commit. The formatting hook still ran. I cleared the PowerShell `SKIP` variable immediately afterward; the repair commit runs both hooks normally.

## Questions I might get from the TA

**Why do tests pass while lint fails?**  
The original tests only exercise two calls to `add`. They do not check shared history, the extra running-total function, or the deliberately broken function. They establish the behavior they actually execute.

**How is linting different from formatting?**  
Linting identifies patterns such as undefined names and unused variables. Formatting standardizes layout. Well-formatted code can still contain a bug.

**Why did `--fix` leave two findings?**  
Only the unused import had a safe automatic fix in this sample. F841 and B006 require care about behavior, so I reviewed and repaired them without enabling unsafe fixes or suppressing the rules.

**Does `None` stop the function from keeping history?**  
No. Omitted history starts a fresh list; explicitly passing a list preserves and extends it. Both behaviors are intentional.

**Why is B015 useful here?**  
It catches valid Python that gives the wrong answer. The call before and after the repair makes the effect visible: the total updates from 12 to 20 only after fixing the assignment.

**Would adding `assert` fix my B015 example?**  
An assertion would check a condition. This function needs to update a total, so assignment matches the intended behavior.

**Why did the normal commit fail?**  
The installed pre-commit lint hook found F821 and exited nonzero, so Git did not create the attempted commit. The formatting hook could still pass.

**Why use CI if a hook already checks the code?**  
A developer can skip a hook or never install it. CI checks the code independently on the PR. This demonstration skips local lint once and lets CI catch the same defect.

**Does a red check by itself prevent merging?**  
No. The active ruleset makes the named status checks required on the target branch. The report records the failed check and the merge state.

**Why repair the same PR?**  
It keeps the defect and repair in one review. Pushing to the same branch updates that PR and reruns CI on its new commit.

**Why avoid `--no-verify`?**  
The exercise only needs to skip lint once. `SKIP=ruff-check` keeps the formatting hook active; `--no-verify` would skip the whole pre-commit hook.

**Where can I inspect the evidence?**  
`evidence/logs` preserves actual commands, output, exit codes, timestamps, and calculator source snapshots. The numbered report maps those records to the ten submission items. GitHub run and PR links allow direct inspection of the hosted checks.

## Submission

The handout asks for **one PDF on Quercus**, containing ten numbered items. A repository URL alone is insufficient. Review the report and its completion notes before uploading, and be ready to explain the extra rule during the TA oral check.

Publishing to GitHub and creating a report do not submit it to Quercus or complete the oral demonstration.
