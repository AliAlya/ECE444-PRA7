"""Build the numbered PRA7 report from preserved evidence, without inventing images."""

import json
import re
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image as PillowImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / "evidence" / "logs"
SHOTS = ROOT / "evidence" / "screenshots"
REPO = "https://github.com/AliAlya/ECE444-PRA7"
BASELINE = f"{REPO}/actions/runs/44465783555"
FAILED = f"{REPO}/actions/runs/44466075166"
REPAIRED = f"{REPO}/actions/runs/44466570039"
PR = f"{REPO}/pull/1"
RULESET = f"{REPO}/rules/27612614"


def record(name):
    return json.loads((LOGS / f"{name}.json").read_text(encoding="utf-8-sig"))


def transcript(name):
    return (LOGS / f"{name}.txt").read_text(encoding="utf-8-sig")


def source_url(filename):
    return f"{REPO}/blob/demonstrate-ruff/evidence/logs/{filename}"


SECTIONS = [
    {
        "title": "My fork and the practical",
        "text": [
            "Ali Alyaseri | ECE444 PRA7 | November 19, 2026",
            "I used the calculator to follow mistakes through manual linting, a local commit hook, and a pull request. The two starter tests passed during both lint-failure demonstrations. After recording the failures, I added regression tests for the behavior those tests had missed.",
            "The supplied pyproject.toml is unchanged. Local Python and CI use 3.15.2; Ruff is pinned to 0.17.4, pre-commit to 4.7.0, and pytest to 9.2.0.",
        ],
        "links": [("My fork", REPO), ("Demonstration and repair: PR #1", PR)],
        "summary": True,
    },
    {
        "title": "The three initial lint findings",
        "text": [
            "I replaced calculator.py with the supplied flawed sample. Ruff found F401 (unused import), F841 (unused variable), and B006 (mutable default argument). The original two addition tests still passed because they did not exercise record or inspect unused names.",
            "This shows the limit of the original tests: checking two addition results does not establish that every function is free of problems.",
        ],
        "logs": [("Initial lint output", "04-item2-lint-before")],
        "sources": ["05-item2-tests-still-pass.json"],
        "shots": ["item02-lint-before"],
    },
    {
        "title": "What the safe automatic fix changed",
        "text": [
            "I ran Ruff with --fix. It removed the unused os import, leaving F841 and B006. The command exited with code 1 because those findings were still unresolved.",
            "I reviewed the remaining code instead of turning on unsafe fixes or suppressing the checks. Removing an arbitrary assignment can remove side effects; changing a default argument can change behavior. Those repairs need an understanding of the function.",
        ],
        "logs": [("Safe fix output", "06-item3-safe-fix")],
        "shots": ["item03-safe-fix"],
    },
    {
        "title": "My manual repair and formatting check",
        "text": [
            "I removed unused = 123 and changed history=[] to history=None, creating a new list only when history is None. This keeps unrelated calls separate while preserving a list intentionally passed by the caller.",
            "I used is None rather than a truthiness check so an explicitly supplied empty history list is still updated. Ruff then passed. I also applied the handout's poorly spaced add function and confirmed the formatter reported one file reformatted.",
        ],
        "code": [("Repaired calculator at this stage", "07-item4-repaired")],
        "logs": [
            ("Passing lint output", "07-item4-repaired"),
            ("Formatting demonstration", "09-formatting-demo"),
        ],
        "shots": ["item04-repaired"],
    },
    {
        "title": "My additional violation: B015",
        "text": [
            "I added add_to_total(total, value), but used total == add(total, value). That expression compares values and discards the Boolean result. It never updates total. Ruff reported B015, and add_to_total(12, 8) returned 12 instead of 20.",
            "I changed == to =. The same call then returned 20 and Ruff passed. An assertion would not match the function's purpose; this operation needs to update the running total.",
        ],
        "snippets": [
            (
                "Before",
                "def add_to_total(total, value):\n    total == add(total, value)\n    return total",
            ),
            (
                "After",
                "def add_to_total(total, value):\n    total = add(total, value)\n    return total",
            ),
        ],
        "logs": [
            ("Before: B015", "10-item5-b015-before"),
            ("After: lint passes", "12-item5-b015-after"),
        ],
        "sources": ["11-item5-wrong-result.json", "13-item5-correct-result.json"],
        "shots": ["item05-before", "item05-after"],
    },
    {
        "title": "The working GitHub Actions baseline",
        "text": [
            "I copied the supplied CI template and replaced its three TODO commands. The lint job runs Ruff with GitHub annotations, the format job uses --check, and the tests job runs pytest with --maxfail=1. The remaining workflow settings are unchanged.",
            "Each job checks out the repository, configures Python, and installs dependencies independently because jobs run on separate machines. The baseline run completed with all three jobs successful.",
        ],
        "links": [("Specific passing baseline run", BASELINE)],
        "jobs": "18-baseline-ci",
        "shots": ["item06-baseline-ci"],
    },
    {
        "title": "F821 and the rejected commit",
        "text": [
            "On demonstrate-ruff, I appended the required broken_total function. missing_total is undefined. Ruff caught F821 at calculator.py:18:12, while the original two addition tests passed. Merely importing the function does not execute its body.",
            "A normal commit was rejected by ruff-check; ruff-format passed. For the subsequent demonstration commit only, I set SKIP to ruff-check, left formatting active, and cleared SKIP immediately afterward. This let CI independently inspect the same defect.",
        ],
        "snippets": [
            ("Deliberate defect", "def broken_total():\n    return missing_total")
        ],
        "logs": [
            ("Manual lint failure", "20-item7-f821"),
            ("Starter tests", "21-item7-tests"),
            ("Normal commit rejected", "22-item7-rejected-commit"),
        ],
        "sources": ["23-demonstration-skip.json"],
        "shots": ["item07-code", "item07-f821-tests", "item07-rejected-commit"],
    },
    {
        "title": "Requiring successful checks on main",
        "text": [
            "I saved require-ci-on-main on my own fork after the baseline workflow ran. The ruleset is active, targets the default branch (main), requires a pull request, and requires lint, format, and tests. Required approvals are zero for this individual exercise.",
            "The bypass list is empty. Requiring the branch to be up to date is disabled, and checks are enforced on creation. The active-rules endpoint confirmed the rules apply to main. During the intentional failure, GitHub reported the PR merge state as BLOCKED.",
        ],
        "links": [("Saved ruleset", RULESET)],
        "ruleset": True,
        "sources": ["17-ruleset-saved.json", "24-main-active-rules.json"],
        "shots": ["item08-ruleset"],
    },
    {
        "title": "CI catches the failing pull request",
        "text": [
            "I opened PR #1 from demonstrate-ruff into my own fork's main. At commit 95a963e, lint failed, format passed, and tests passed. The saved PR record shows BLOCKED, so the failed required check prevented merging.",
            "The failed job's expanded Ruff log identifies the exact undefined name and file/line reference. The historical run and job remain inspectable after the repair.",
        ],
        "links": [
            ("Same pull request", PR),
            ("Historical failed CI run", FAILED),
            ("F821 lint job", f"{FAILED}/job/135364052312"),
        ],
        "jobs": "26-item9-failing-ci",
        "job_error": True,
        "sources": ["25-item9-failing-pr.json", "27-item9-f821-job.txt"],
        "shots": ["item09-failed-summary", "item09-f821-log"],
    },
    {
        "title": "Repairing the same PR",
        "text": [
            "I repaired broken_total to return add_to_total(12, 8), which evaluates to 20, then pushed to the same demonstrate-ruff branch. Both local hooks ran normally. The repaired run has successful lint, format, and tests jobs; the same PR became CLEAN.",
            "After capturing the two-test failure demonstration, I added four regression tests: independent default histories, preservation of a supplied empty history list, updating an existing total, and calling the repaired function. The final suite has six passing tests.",
            "I left PR #1 open for TA review. The handout requires a repaired passing PR and does not explicitly require merging it. Quercus upload and the oral explanation remain personal submission steps.",
        ],
        "links": [("Repaired PR", PR), ("Specific repaired CI run", REPAIRED)],
        "jobs": "33-item10-repaired-ci",
        "logs": [("Final local tests", "31-repair-tests")],
        "sources": [
            "29-repair-lint.json",
            "30-repair-format-check.json",
            "34-item10-repaired-pr.json",
        ],
        "shots": ["item10-repaired-pr"],
    },
]

STYLES = getSampleStyleSheet()
STYLES.add(
    ParagraphStyle(
        "ReportBody", fontName="Helvetica", fontSize=9.5, leading=13, spaceAfter=7
    )
)
STYLES.add(
    ParagraphStyle(
        "ReportTitle",
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#173d51"),
        spaceAfter=16,
    )
)
STYLES.add(
    ParagraphStyle(
        "ReportSub",
        fontName="Helvetica-Bold",
        fontSize=10.2,
        leading=14,
        spaceBefore=9,
        spaceAfter=5,
    )
)
STYLES.add(
    ParagraphStyle(
        "ReportSmall",
        fontName="Helvetica",
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor("#52606a"),
        spaceAfter=5,
    )
)
STYLES.add(
    ParagraphStyle(
        "ReportCode",
        fontName="Courier",
        fontSize=7.5,
        leading=9,
        spaceBefore=4,
        spaceAfter=7,
        backColor=colors.HexColor("#f3f6f8"),
        borderPadding=8,
        alignment=TA_LEFT,
    )
)


def paragraph(text, style="ReportBody"):
    return Paragraph(escape(text), STYLES[style])


def code_block(text):
    text = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", text).replace("\ufeff", "")
    lines = []
    for line in text.splitlines():
        lines.extend(
            textwrap.wrap(
                line, width=104, replace_whitespace=False, drop_whitespace=False
            )
            or [""]
        )
    return Preformatted("\n".join(lines), STYLES["ReportCode"])


def screenshot_files(prefix):
    return sorted(SHOTS.glob(f"{prefix}.png")) + sorted(SHOTS.glob(f"{prefix}-*.png"))


def table(rows, widths=None):
    cells = [[paragraph(str(cell), "ReportSmall") for cell in row] for row in rows]
    result = Table(cells, colWidths=widths, hAlign="LEFT", repeatRows=1)
    result.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6eff3")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#d3dde2")),
            ]
        )
    )
    return result


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#ccd7df"))
    canvas.line(48, 39, 564, 39)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#52606a"))
    canvas.drawString(48, 26, "Ali Alyaseri | ECE444 PRA7 | Evidence report")
    canvas.drawRightString(564, 26, f"Page {doc.page}")
    canvas.restoreState()


def build():
    missing = [
        (index, name)
        for index, section in enumerate(SECTIONS, 1)
        for name in section.get("shots", [])
        if not screenshot_files(name)
    ]
    draft = bool(missing)
    output = ROOT / "output" / "pdf"
    output.mkdir(parents=True, exist_ok=True)
    suffix = "_DRAFT" if draft else ""
    pdf = output / f"Ali_Alyaseri_PRA7_Report{suffix}.pdf"
    document = SimpleDocTemplate(
        str(pdf),
        pagesize=letter,
        rightMargin=48,
        leftMargin=48,
        topMargin=43,
        bottomMargin=53,
        title="ECE444 PRA7 - Ali Alyaseri",
        author="Ali Alyaseri",
    )
    story = []
    markdown = ["# ECE444 PRA7 - Ali Alyaseri", "", "November 19, 2026", ""]
    if draft:
        note = "DRAFT - required screenshots still need to be inserted. All command output and GitHub results below come from saved execution/API records; they are transcripts and structured records, not terminal or browser screenshots. See evidence/CAPTURE_CHECKLIST.md before submitting."
        markdown += [f"**{note}**", ""]
    for index, section in enumerate(SECTIONS, 1):
        if index > 1:
            story.append(PageBreak())
        story += [
            paragraph("ECE444 / STATIC ANALYSIS AND CI", "ReportSmall"),
            paragraph(f"{index}. {section['title']}", "ReportTitle"),
        ]
        markdown += [f"## {index}. {section['title']}", ""]
        if index == 1 and draft:
            story += [paragraph(note), Spacer(1, 6)]
        for text in section["text"]:
            story.append(paragraph(text))
            markdown += [text, ""]
        for label, url in section.get("links", []):
            story.append(
                Paragraph(
                    f'<b>{escape(label)}:</b> <link href="{escape(url)}" color="#146b8c">{escape(url)}</link>',
                    STYLES["ReportSmall"],
                )
            )
            markdown += [f"[{label}]({url})", ""]
        if section.get("summary"):
            story += [
                Spacer(1, 12),
                table(
                    [
                        ["Stage", "Observed result"],
                        ["Baseline", "lint / format / tests: successful"],
                        [
                            "Deliberate F821",
                            "lint failed; format and 2 tests passed; merge BLOCKED",
                        ],
                        [
                            "Repair",
                            "all three jobs successful; 6 tests passed; merge CLEAN",
                        ],
                        [
                            "Submission evidence",
                            "Screenshots pending"
                            if draft
                            else "Required screenshot files supplied",
                        ],
                    ],
                    [118, 398],
                ),
                Spacer(1, 18),
                paragraph("Evidence provenance", "ReportSub"),
                paragraph(
                    "The numbered items follow the handout. Raw command records contain the actual arguments, output, exit status, timestamp, and calculator source. GitHub records preserve the baseline, failed, and repaired runs. No failed state was recreated by editing a screenshot."
                ),
            ]
        for label, name in section.get("code", []):
            value = record(name)["calculator"].strip("\n")
            story += [paragraph(label, "ReportSub"), code_block(value)]
            markdown += [f"### {label}", "", "```python", value.rstrip(), "```", ""]
        for label, value in section.get("snippets", []):
            story += [paragraph(label, "ReportSub"), code_block(value)]
            markdown += [f"### {label}", "", "```python", value, "```", ""]
        if section.get("jobs"):
            value = record(section["jobs"])
            rows = [["Job", "Conclusion", "Completed (UTC)"]] + [
                [job["name"], job["conclusion"], job["completedAt"]]
                for job in value["jobs"]
            ]
            story += [
                paragraph("Saved GitHub job results", "ReportSub"),
                table(rows, [100, 120, 296]),
                paragraph(f"Source: {section['jobs']}.json", "ReportSmall"),
            ]
            markdown += (
                ["| Job | Conclusion | Completed (UTC) |", "| --- | --- | --- |"]
                + [f"| {' | '.join(row)} |" for row in rows[1:]]
                + [""]
            )
        if section.get("ruleset"):
            value = record("17-ruleset-saved")
            rows = [
                ["Setting", "Saved value"],
                ["Name", value["name"]],
                ["Enforcement", value["enforcement"]],
                ["Target", "Default branch: main"],
                ["Bypass actors", str(value["bypass_actors"])],
                ["Pull request", "Required; approvals: 0"],
                ["Required checks", "lint, format, tests"],
                ["Require up-to-date branch", "No"],
                ["Skip checks on creation", "No"],
            ]
            story += [table(rows, [185, 331])]
            markdown += (
                ["| Setting | Saved value |", "| --- | --- |"]
                + [f"| {' | '.join(row)} |" for row in rows[1:]]
                + [""]
            )
        for label, name in section.get("logs", []):
            value = transcript(name)
            story += [
                paragraph(f"{label} - saved command transcript", "ReportSub"),
                code_block(value),
                Paragraph(
                    f'<link href="{escape(source_url(name + ".json"))}" color="#146b8c">Source record: {escape(name)}.json</link>',
                    STYLES["ReportSmall"],
                ),
            ]
            markdown += [
                f"### {label} (saved command transcript)",
                "",
                "```text",
                value.rstrip(),
                "```",
                "",
                f"[Source record](evidence/logs/{name}.json)",
                "",
            ]
        if section.get("job_error"):
            lines = transcript("27-item9-f821-job").splitlines()
            error = "\n".join(
                line.split("\t", 2)[-1]
                for line in lines
                if "##[group]Run python" in line or "##[error]" in line
            )
            story += [
                paragraph("Excerpt from the actual failed job log", "ReportSub"),
                code_block(error),
            ]
            markdown += ["```text", error, "```", ""]
        for filename in section.get("sources", []):
            story.append(
                Paragraph(
                    f'<link href="{escape(source_url(filename))}" color="#146b8c">Additional source: {escape(filename)}</link>',
                    STYLES["ReportSmall"],
                )
            )
            markdown += [
                f"[Additional source: {filename}](evidence/logs/{filename})",
                "",
            ]
        section_missing = [
            name for name in section.get("shots", []) if not screenshot_files(name)
        ]
        if section_missing:
            story.append(
                paragraph(
                    "Required screenshots pending for this item; see the capture checklist. The saved records above do not replace them.",
                    "ReportSmall",
                )
            )
        for prefix in section.get("shots", []):
            files = screenshot_files(prefix)
            if not files:
                markdown += [
                    f"**Required screenshot pending:** `evidence/screenshots/{prefix}.png`.",
                    "",
                ]
            for file in files:
                with PillowImage.open(file) as image:
                    width, height = image.size
                scale = min(516 / width, 590 / height)
                story.append(
                    KeepTogether(
                        [
                            paragraph(file.name, "ReportSmall"),
                            Image(
                                str(file), width=width * scale, height=height * scale
                            ),
                        ]
                    )
                )
                markdown += [f"![{file.stem}](evidence/screenshots/{file.name})", ""]
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    (ROOT / "REPORT.md").write_text("\n".join(markdown), encoding="utf-8")
    print(pdf)
    print(f"Required screenshot groups missing: {len(missing)}")


if __name__ == "__main__":
    build()
