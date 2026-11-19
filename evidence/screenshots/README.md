# Screenshot provenance

Fourteen PNG files cover the thirteen required image groups. The ruleset uses two images so both its overall settings and expanded required checks are readable.

All images were captured from actual Windows Chrome windows using the computer-use capture API. They were cropped to remove unrelated tabs and blank space. Cropping did not change results, code, check statuses, or labels.

## Direct GitHub page captures

- `item06-baseline-ci.png`: the original successful baseline run.
- `item08-ruleset.png` and `item08-ruleset-2.png`: the public saved ruleset, Active enforcement, default branch target, and expanded lint/format/tests requirements.
- `item09-failed-summary.png`: PR #1's historical checks at failing commit `95a963e`, with lint failing and format/tests succeeding.
- `item10-repaired-pr.png`: the same PR's successful checks after the repair and README update.

## Captures of original saved output

The remaining images are browser screenshots of the readable source sheets in `evidence/pages/`. Each sheet identifies the original JSON or text record. The command, output, exit code, and calculator source come from those original records. They are not screenshots of a live terminal session.

`item09-f821-log.png` displays the actual saved failed job output from `gh run view --log-failed`, including the Ruff step, F821 at `calculator.py:18:12`, and exit code 1. The browser was signed out of GitHub, which requires sign-in for its full log view, so this is a captured saved-log view rather than an expanded signed-in GitHub log panel. Redundant job/step prefixes were removed for readable display; timestamps and log messages were preserved.

The original records in `evidence/logs/` remain unchanged. The source sheets and image labels make the capture method explicit. The PDF repeats this distinction on its first page. If a TA requires the original terminal frame or signed-in GitHub log panel specifically, use the replay commands and source links in [the capture checklist](../CAPTURE_CHECKLIST.md) to replace those captures.
