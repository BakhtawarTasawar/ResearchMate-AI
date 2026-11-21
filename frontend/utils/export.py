"""
Report generation utilities — export structured analysis to Markdown.
"""
from __future__ import annotations

import datetime


def generate_markdown_report(
    results: dict,
    original_text: str,
    model_name: str = "ResearchGate Assistant",
    title: str = "ResearchGate AI — Structured Scientific Analysis",
) -> str:
    """Generate a clean, structured Markdown report from analysis results."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    summary = results.get("summary", "Not stated in the abstract.")
    objectives = results.get("objectives", [])
    findings = results.get("findings", [])
    keywords = results.get("keywords", [])
    questions = results.get("questions", [])

    lines = [
        f"# {title}",
        "",
        f"- **Generated:** {timestamp}",
        f"- **Platform:** ResearchGate AI Institutional Assistant",
        f"- **Word Count (Source):** ~{len(original_text.split()):,} words",
        f"- **Character Count (Source):** {len(original_text):,} characters",
        "",
        "---",
        "",
        "## 1. Simple Summary",
        "> *Accessible plain-language synthesis of problem, methodology, and conclusion.*",
        "",
        summary,
        "",
        "---",
        "",
        "## 2. Research Objectives",
        "> *Core hypotheses and investigated research questions.*",
        "",
    ]

    for obj in objectives:
        lines.append(f"- {obj}")

    lines.extend([
        "",
        "---",
        "",
        "## 3. Key Findings",
        "> *Empirical discoveries, quantitative metrics, and measured outcomes.*",
        "",
    ])

    for f in findings:
        lines.append(f"- {f}")

    lines.extend([
        "",
        "---",
        "",
        "## 4. Important Keywords",
        "> *Scientific concept tags and domain ontology.*",
        "",
        ", ".join(keywords) if keywords else "None extracted.",
        "",
        "---",
        "",
        "## 5. Future Research Questions",
        "> *Analytical research frontiers, limitations, and follow-up hypotheses.*",
        "",
    ])

    for q in questions:
        lines.append(f"- {q}")

    lines.extend([
        "",
        "---",
        "",
        "## Source Abstract / Extracted Text",
        "",
        "```text",
        original_text.strip(),
        "```",
        "",
        "---",
        "*Notice: AI-generated research insights should be reviewed and verified against primary literature.*",
    ])

    return "\n".join(lines)


def format_dimension_text(key: str, results: dict) -> str:
    """Format an individual dimension as clean Markdown for quick copying."""
    if key == "summary":
        return results.get("summary", "")
    elif key == "keywords":
        return ", ".join(results.get("keywords", []))
    items = results.get(key, [])
    return "\n".join(f"- {item}" for item in items)
