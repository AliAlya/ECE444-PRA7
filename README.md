# ECE444 PRA7 - Catching mistakes before they get merged

Ali Alyaseri | [AliAlya/ECE444-PRA7](https://github.com/AliAlya/ECE444-PRA7)

**[Download/view the final submission PDF](output/pdf/Ali_Alyaseri_PRA7_Report.pdf)** | **[Download the project ZIP](https://github.com/AliAlya/ECE444-PRA7/archive/refs/heads/main.zip)**

The PDF, all 14 screenshots, report source, evidence records, and project code are saved in this repository. I can retrieve them from GitHub without access to the original computer. Use GitHub's download button when viewing the PDF, then upload that file to Quercus.

This practical uses a small calculator to follow a mistake through a manual Ruff check, a local Git hook, and a GitHub pull request. The interesting result is that the original two tests can pass while Ruff still identifies a problem. Each check sees a different part of the code.

Based on the [PRA7 handout](https://shuruizuoft.github.io/ECE444-Fall2026/pras/static-analysis-ci.html) and forked from the [course starter](https://github.com/shuruizUofT/ece444-pra7-starter). The supplied Ruff configuration and tool versions are preserved.

## Start here: what I run, show, and submit

**What this project is:** a Python calculator module, tests, and automated code checks. The practical is about finding and repairing mistakes. There is no server to start. Running `calculator.py` on its own defines its functions and normally prints nothing.

**Where my finished work is:** `main`, with the full demonstration history in [PR #1](https://github.com/AliAlya/ECE444-PRA7/pull/1). The `demonstrate-ruff` branch is retained for the historical evidence links. A normal clone checks out the completed project on `main`.

**My quick run in PowerShell:**

```powershell
git branch --show-current
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
```

Run these from the cloned project folder after completing the setup below. The branch should be `main`. Expect **6 passed**, **All checks passed!**, and a message that the files are already formatted. The preserved `demonstrate-ruff` branch also contains the completed work.

**What I should be ready to show the TA:**

1. The calculator and the six tests, with the checks above passing.
2. My extra **B015** example: `==` left the total at 12; changing it to `=` made adding 8 return 20. Explain the code, finding, and repair.
3. The F401/F841/B006 findings, what Ruff fixed automatically, and why I repaired the rest manually.
4. The deliberate **F821** defect: the two starter tests passed while lint and the normal commit failed.
5. The failed GitHub run, the active ruleset requiring all three checks, and the **same repaired PR** with passing checks.

The handout explicitly asks me to be prepared for an oral test on my additional violation. The sequence above is my preparation guide for explaining the whole practical; it is not a separate slide-deck requirement.

**What I submit:** one PDF through **Quercus**, containing the ten numbered report items, screenshots, and required links. Screenshots have been added to `output/pdf/Ali_Alyaseri_PRA7_Report.pdf`. Review the final PDF and its capture-provenance note before uploading. A GitHub push does not submit it to Quercus.

For the details, use [the TA walkthrough](#my-walkthrough-for-the-ta), [Windows commands](#run-it-on-my-windows-computer), [the ten report items](#what-goes-in-the-pdf-and-how-i-finish-it), and [questions with answers](#questions-i-might-get-from-the-ta).

## Using another computer

To retrieve the submission, I only need the PDF link at the top of this README. To run the code, install Git and Python 3.15, then clone the repository. On Windows, the Python launcher should recognize `py -3.15`.

```powershell
git clone https://github.com/AliAlya/ECE444-PRA7.git
Set-Location ECE444-PRA7
py -3.15 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pre_commit install
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
```

The local run used Python 3.15.2. If `py -3.15` is unavailable, install Python 3.15 first; the old computer's `.tools/python315` directory is not part of the repository. Virtual environments are recreated rather than copied between machines.

On macOS/Linux, create the environment with `python3.15 -m venv .venv`, then use `.venv/bin/python` in place of `.\.venv\Scripts\python.exe` in the commands above.

To rebuild the PDF on the new Windows computer, use a separate report environment:

```powershell
py -3.15 -m venv .report-venv
.\.report-venv\Scripts\python.exe -m pip install -r requirements-report.txt
.\.report-venv\Scripts\python.exe tools/build_report.py
```

The existing screenshots and records are included, so rebuilding does not require retaking them or signing into GitHub. Clone with Git if I want to use the replay helper: it reads the original starter tests from Git history, which is absent from a downloaded ZIP.

## Verified result

| Stage | Result and evidence |
| --- | --- |
| Working baseline | All three jobs passed: [baseline run](https://github.com/AliAlya/ECE444-PRA7/actions/runs/44465783555). |
| Intentional defect | F821 failed lint; formatting and the two starter tests passed: [failed run](https://github.com/AliAlya/ECE444-PRA7/actions/runs/44466075166). GitHub reported the PR merge state as `BLOCKED`. |
| Repair | All three jobs passed: [repaired run](https://github.com/AliAlya/ECE444-PRA7/actions/runs/44466570039). The same PR became `CLEAN`. |
| Branch protection | [require-ci-on-main](https://github.com/AliAlya/ECE444-PRA7/rules/27612614) is active; its bypass list is empty and all three checks are required. |
| Pull request | [PR #1](https://github.com/AliAlya/ECE444-PRA7/pull/1) preserves the failed and repaired checks; completed work is merged into `main` for access from another computer. The earlier screenshots show the PR before merging. |
| Local final code | Ruff lint and formatting pass. **6 tests pass**, including four regression tests added after the failure demonstration. |

**Submission status:** the code, GitHub demonstration, and report images are complete. The [numbered report](REPORT.md) includes 14 screenshots. GitHub summaries and ruleset pages were captured directly; local code/output and the failed CI log were captured from browser views of the original saved records. Those images are labeled as saved records, not live terminal or signed-in log-panel captures. See [screenshot provenance](evidence/screenshots/README.md). Quercus upload and the TA explanation remain personal steps.

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

Open the cloned project folder in VS Code and use its PowerShell terminal, or enter that folder in a regular PowerShell window. For example, if I cloned into the current directory:

```powershell
Set-Location ECE444-PRA7
```

Use the environment's executable directly. Activation and PowerShell execution-policy changes are unnecessary.

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

### See the calculator functions actually run

This command calls the functions and prints their results:

```powershell
.\.venv\Scripts\python.exe -c "from calculator import add, add_to_total, broken_total, record; print('2 + 3 =', add(2, 3)); print('12 + 8 =', add_to_total(12, 8)); print('Separate histories:', record(12), record(8)); history = []; record(12, history); record(8, history); print('Shared history supplied by caller:', history); print('Repaired total:', broken_total())"
```

Expected output:

```text
2 + 3 = 5
12 + 8 = 20
Separate histories: [12] [8]
Shared history supplied by caller: [12, 8]
Repaired total: 20
```

To show the individual tests and their names:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

### If a command does not work

| What I see | What I check |
| --- | --- |
| `.venv\Scripts\python.exe` cannot be found | Run from the PRA7 folder. If the environment is missing, use the recreation commands above. |
| `No module named pytest`, `ruff`, or `pre_commit` | Use this project's `.venv` executable and install `requirements-dev.txt` into that environment. |
| Only 2 tests run | I may be viewing an older baseline commit. Fetch/pull the completed `main` branch; the final project has six tests. |
| A replay reports lint errors or a rejected commit | That is expected for the failing stages. The helper checks that the failure happened and keeps it in a separate scratch folder. |
| A hook reformats a file | Review the change, stage it again, and retry. A modifying hook intentionally asks for another pass. |

## My walkthrough for the TA

Before the session, have the final branch open locally, the report available, and these browser tabs ready: [PR #1](https://github.com/AliAlya/ECE444-PRA7/pull/1), [the failed run](https://github.com/AliAlya/ECE444-PRA7/actions/runs/44466075166), and [the ruleset](https://github.com/AliAlya/ECE444-PRA7/rules/27612614). The historical failed run stays available even though the PR is now repaired.

### 1. Explain the purpose and show the final checks

My opening explanation can be:

> I used Ruff to find source-code problems, pre-commit to catch them before a commit, and GitHub Actions to check the pushed changes independently. I deliberately showed tests passing while lint failed, then repaired the code and added tests for the missed behavior.

Run pytest, Ruff lint, and the formatting check from the quick-run block. Open `calculator.py` and `test_calculator.py` so I can connect each result to the code. Be clear that the final six-test suite was added after the original two-test failure demonstrations.

### 2. Explain the original findings and repairs

Use report items 2-4 or the saved evidence to show F401, F841, and B006. Explain that the safe fixer removed `os`, I removed the unused assignment, and `None` prevents unrelated `record` calls from sharing a default list.

If asked to reproduce those stages live, run the isolated helpers one at a time:

```powershell
.\.venv\Scripts\python.exe tools/replay_evidence.py item2
.\.venv\Scripts\python.exe tools/replay_evidence.py item3
.\.venv\Scripts\python.exe tools/replay_evidence.py item4
```

These run the real commands using the saved source states in fresh scratch folders. They leave my final calculator and PR branch intact. Say explicitly that these are replays; the original timestamped outputs are in `evidence/logs/`.

### 3. Spend time on my additional B015 rule

Run these separately so the before and after are easy to compare:

```powershell
.\.venv\Scripts\python.exe tools/replay_evidence.py item5-before
.\.venv\Scripts\python.exe tools/replay_evidence.py item5-after
```

Point to the discarded comparison, the B015 message, and the actual result of 12. Then point to the assignment, passing lint, and the corrected result of 20. Explain why assignment matches the intended operation. This is the additional rule I must be ready to discuss orally.

### 4. Show the local commit being rejected

```powershell
.\.venv\Scripts\python.exe tools/replay_evidence.py item7
```

The helper creates an isolated local Git repository, installs the hook, and attempts the defective commit. Show `missing_total`, F821, **2 passing tests**, and the rejected commit. The formatting hook still passes. The rejected commit is the expected demonstration result.

Explain that the original tests never called `broken_total`. The real hosted failure was committed once by skipping only `ruff-check`; formatting still ran and the temporary `SKIP` setting was removed afterward.

### 5. Connect the local result to GitHub enforcement

Open the [failed lint job](https://github.com/AliAlya/ECE444-PRA7/actions/runs/44466075166/job/135364052312) and expand the Ruff step. Identify `calculator.py:18:12` and F821. Show that the failed run had successful format and tests jobs.

Then show the active `require-ci-on-main` ruleset: default branch target, required PR, zero approvals, required `lint`/`format`/`tests`, and an empty bypass list. Explain that the saved failed PR state was `BLOCKED`; a red check becomes a merge requirement through this ruleset.

Finish on [the same repaired PR](https://github.com/AliAlya/ECE444-PRA7/pull/1), with all three checks passing. Show the repaired function and its new regression test. The PR is merged so the completed work is available on `main`; its original failed runs, repaired runs, commits, and pre-merge screenshots remain available for review.

## What goes in the PDF and how I finish it

| Report item | Required content |
| --- | --- |
| 1 | My fork's repository URL; no setup screenshot is required. |
| 2 | Screenshot of the original lint command and all F401, F841, B006 findings. |
| 3 | Screenshot of the safe auto-fix command and its output. |
| 4 | Repaired calculator code and screenshot of passing lint. |
| 5 | My B015 code and lint output before and after repair, with a brief explanation. |
| 6 | Screenshot of the passing baseline's three jobs and the specific Actions run URL. |
| 7 | Broken function plus terminal screenshots showing F821, passing tests, and the rejected commit. |
| 8 | Saved ruleset screenshots showing its name, Active status, target branch, and three required checks; include its URL if available. |
| 9 | Failed PR/check summary and expanded failed lint log showing F821 with the file/line reference. |
| 10 | The same repaired PR's URL and screenshot showing all three jobs passing. |

The screenshots are saved in `evidence/screenshots/`. The [capture checklist](evidence/CAPTURE_CHECKLIST.md) retains the exact image filenames, direct GitHub links, and replay commands if I want to replace a saved-output capture with a live terminal capture. After changing any images, rebuild:

```powershell
.\.report-venv\Scripts\python.exe tools/build_report.py
```

The builder updates `REPORT.md` and writes the PDF to `output/pdf/`. While mandatory screenshot groups are missing, it produces `Ali_Alyaseri_PRA7_Report_DRAFT.pdf`. When all required groups are supplied, it produces `Ali_Alyaseri_PRA7_Report.pdf`. The presence of an image does not establish that it shows the right content: I still need to open the PDF, check legibility and completeness, and upload the final version through Quercus.

The final `output/pdf/Ali_Alyaseri_PRA7_Report.pdf` is committed to Git along with the code, screenshots, source sheets, report source, and evidence records. Virtual environments, portable Python, draft PDFs, rendering previews, and scratch replays remain excluded. Check Quercus for the deadline and any additional submission-field instructions; the handout does not provide a deadline or required PDF filename.

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
