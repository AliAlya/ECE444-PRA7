# PRA7 screenshot checklist

The actual activities, outputs, CI runs, and ruleset are saved. Screenshots remain necessary because the handout explicitly requests them. Browser automation ended when it could not reliably identify the current URL, so none of the saved text records is being presented as a genuine terminal or GitHub screenshot.

Put PNG screenshots in `evidence/screenshots/` with the filenames below. The report builder will include each supplied image automatically. Use readable captures and multiple images where needed. The raw `.txt` and `.json` records remain in `evidence/logs/`.

| Item | Filename(s) | What the capture must show |
| --- | --- | --- |
| 2 | `item02-lint-before.png` | Command and all F401, F841, B006 findings. The genuine original output is in `04-item2-lint-before.txt`. |
| 3 | `item03-safe-fix.png` | `ruff check --fix calculator.py` and its output: 1 fixed, 2 remaining. See `06-item3-safe-fix.txt`. |
| 4 | `item04-repaired.png` | Repaired code and passing lint command/output. The source at this stage is in `07-item4-repaired.json`. |
| 5 | `item05-before.png`, `item05-after.png` | B015 code and lint output before and after repair. Source and output are in `10-item5-b015-before.json` and `12-item5-b015-after.json`. |
| 6 | `item06-baseline-ci.png` | [Baseline run](https://github.com/AliAlya/ECE444-PRA7/actions/runs/44465783555) with lint, format, and tests passing. |
| 7 | `item07-code.png`, `item07-f821-tests.png`, `item07-rejected-commit.png` | Broken function, F821, two passing tests, and the rejected normal commit. See records 20, 21, and 22. |
| 8 | `item08-ruleset.png`, optionally `item08-ruleset-2.png` | [Saved ruleset settings](https://github.com/AliAlya/ECE444-PRA7/settings/rules/27612614): name, Active enforcement, main/default target, and required lint/format/tests checks. |
| 9 | `item09-failed-summary.png`, `item09-f821-log.png` | [Historical failed run](https://github.com/AliAlya/ECE444-PRA7/actions/runs/44466075166) and [failed lint job](https://github.com/AliAlya/ECE444-PRA7/actions/runs/44466075166/job/135364052312), including expanded Ruff step and calculator.py:18:12 F821. For the historical PR checks use [PR checks at the failed job](https://github.com/AliAlya/ECE444-PRA7/pull/1/checks?check_run_id=135364052312). |
| 10 | `item10-repaired-pr.png` | [The same PR](https://github.com/AliAlya/ECE444-PRA7/pull/1) showing all three checks passing. |

Optional extra captures with suffixes such as `item02-lint-before-2.png` are also included. If an image is too tall, use several readable captures rather than squeezing all text into one small image.

## Safely revisiting the local failures

The replay helper performs the actual commands in a new ignored scratch folder. It never pushes, modifies this final calculator, or changes the current branch. Run the relevant command in your terminal, then capture the visible output:

```powershell
.\.venv\Scripts\python.exe tools/replay_evidence.py item2
.\.venv\Scripts\python.exe tools/replay_evidence.py item3
.\.venv\Scripts\python.exe tools/replay_evidence.py item4
.\.venv\Scripts\python.exe tools/replay_evidence.py item5-before
.\.venv\Scripts\python.exe tools/replay_evidence.py item5-after
.\.venv\Scripts\python.exe tools/replay_evidence.py item7
```

Item 7 creates a separate local Git repository with the original two tests and installs the hook there. The commit attempt genuinely fails. Keep `SKIP` unset when running it. First-time hook setup may need internet access. These captures are replays of the same source states; the original timestamped records remain available separately.

The current `demonstrate-ruff` branch contains the repaired code. Do not overwrite it or force-push an older commit merely to recreate screenshots.

The JSON records include the calculator source for each stage. To rerun a stage, make a separate scratch copy of the project outside the final working tree (or under ignored `.tools/replay/`), copy the matching calculator snapshot there, and run the indicated command with the existing `.venv` interpreter. The original two starter tests can be inspected with `git show 98efd77:test_calculator.py`. A separate Git clone is needed to demonstrate an actual rejected commit without changing this completed branch.

Earlier commits are also inspectable without changing branches:

```powershell
git show aa72d60:calculator.py
git show 95a963e:calculator.py
git show ee1855d:calculator.py
```

Records 04 and 06 preserve the initial lint and auto-fix stages, which occurred before the first project commit. They can be rerun from the original flawed sample and supplied configuration.

## Rebuild after adding captures

```powershell
.\.report-venv\Scripts\python.exe tools/build_report.py
```

On a fresh machine, install `requirements-report.txt` into a separate environment first. This is only for document generation; it does not change the assignment's development dependencies or CI jobs.

The PDF remains a draft while mandatory screenshot filenames are missing. After adding them, open the generated PDF and check that every image is legible before submitting it through Quercus. The oral explanation with the TA is still a personal task.
