"""Rerun a local evidence stage in a new scratch folder, preserving the final tree."""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGES = {
    "item2": "04-item2-lint-before",
    "item3": "04-item2-lint-before",
    "item4": "07-item4-repaired",
    "item5-before": "10-item5-b015-before",
    "item5-after": "12-item5-b015-after",
    "item7": "20-item7-f821",
}


def run(folder, arguments, expected=0, show=True):
    if show:
        label = [
            "python" if str(arg) == sys.executable else str(arg) for arg in arguments
        ]
        print(f"\n> {subprocess.list2cmdline(label)}", flush=True)
    result = subprocess.run(arguments, cwd=folder, check=False)
    if result.returncode != expected:
        raise SystemExit(
            f"Expected exit {expected}, got {result.returncode}. Scratch folder: {folder}"
        )


def snapshot(name):
    file = ROOT / "evidence" / "logs" / f"{name}.json"
    return json.loads(file.read_text(encoding="utf-8-sig"))["calculator"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=STAGES)
    arguments = parser.parse_args()
    replay_root = ROOT / ".tools" / "replay"
    replay_root.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix=f"{arguments.stage}-", dir=replay_root))
    for name in ("pyproject.toml", ".pre-commit-config.yaml"):
        shutil.copy2(ROOT / name, folder / name)
    starter_tests = subprocess.check_output(
        ["git", "show", "98efd77:test_calculator.py"], cwd=ROOT
    )
    (folder / "test_calculator.py").write_bytes(starter_tests)
    source = snapshot(STAGES[arguments.stage])
    python = sys.executable
    print(
        f"PRA7 evidence replay: {arguments.stage}\nScratch folder: {folder}", flush=True
    )
    print("Final calculator, branches, and hosted PR are unchanged.\n", flush=True)

    if arguments.stage == "item7":
        (folder / ".gitignore").write_text(
            "__pycache__/\n.pytest_cache/\n.ruff_cache/\n", encoding="utf-8"
        )
        (folder / "calculator.py").write_text(
            snapshot("07-item4-repaired"), encoding="utf-8"
        )
        run(folder, ["git", "init", "-b", "main"], show=False)
        run(folder, ["git", "config", "user.name", "PRA7 evidence replay"], show=False)
        run(
            folder,
            ["git", "config", "user.email", "replay@example.invalid"],
            show=False,
        )
        run(folder, ["git", "add", "."], show=False)
        run(
            folder,
            ["git", "commit", "-m", "Start isolated evidence replay"],
            show=False,
        )
        run(folder, [python, "-m", "pre_commit", "install"])
        (folder / "calculator.py").write_text(source, encoding="utf-8")
        print("\ncalculator.py:\n" + source, flush=True)
        run(folder, [python, "-m", "ruff", "check", "."], expected=1)
        run(folder, [python, "-m", "pytest", "-q"])
        run(folder, ["git", "add", "calculator.py"])
        run(
            folder,
            ["git", "commit", "-m", "Show that the hook catches an undefined total"],
            expected=1,
        )
        print("\nThe commit was rejected as expected. Nothing was pushed.", flush=True)
        return

    (folder / "calculator.py").write_text(source, encoding="utf-8")
    if arguments.stage in ("item4", "item5-before", "item5-after"):
        print("calculator.py:\n" + source, flush=True)
    flags = ["--fix"] if arguments.stage == "item3" else []
    expected = 1 if arguments.stage in ("item2", "item3", "item5-before") else 0
    run(folder, [python, "-m", "ruff", "check", *flags, "calculator.py"], expected)
    if arguments.stage == "item2":
        run(folder, [python, "-m", "pytest", "-q"])
    if arguments.stage in ("item5-before", "item5-after"):
        run(
            folder,
            [
                python,
                "-c",
                "from calculator import add_to_total; print('Starting total: 12; new value: 8'); print('Expected: 20'); print('Actual:', add_to_total(12, 8))",
            ],
        )


if __name__ == "__main__":
    main()
