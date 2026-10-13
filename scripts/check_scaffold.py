"""Minimal starter pack integrity checker; standard library only.

This is NOT an application test or a security scanner.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md", "START_HERE.md", "AGENTS.md", "CLAUDE.md", "AI_USAGE.md",
    "compose.yaml", ".env.example", "backend/.env.example",
    "frontend/.env.example", "docs/PRODUCT_REQUIREMENTS.md",
    "docs/ARCHITECTURE.md", "docs/API_CONTRACT.md", "docs/DATA_MODEL.md",
    "docs/UI_DESIGN.md", "docs/TEST_PLAN.md", "docs/CI_CD.md",
    "docs/PROGRESS.md", "docs/SUBMISSION_CHECKLIST.md",
    ".github/workflows/ci.yml", "prompts/00_AGENT_ONBOARDING.md",
    "prompts/B01_BACKEND_FOUNDATION.md",
)
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"Required file missing: {rel}")

    md_count = 0
    for doc in ROOT.rglob("*.md"):
        if any(part in {"node_modules", ".next", ".venv"} for part in doc.parts):
            continue
        md_count += 1
        content = doc.read_text(encoding="utf-8")
        for match in LINK.finditer(content):
            link = match.group(1).strip().split(" ", 1)[0]
            if not link or link.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path = link.split("#", 1)[0]
            if path and not (doc.parent / path).exists():
                errors.append(f"Broken local Markdown link: {doc.relative_to(ROOT)} -> {path}")

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print(f"Starter checks passed ({len(REQUIRED)} required files, {md_count} Markdown files).")
    print("Note: No application logic or tests are validated by this checker.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
