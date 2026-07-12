"""Convert LaTeX delimiters to GitHub-flavored $ / $$ math.

GitHub README math does not render \\( \\) / \\[ \\]; it expects $ and $$.
Run: python assets/fix_github_math.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "__pycache__", ".pytest_cache", "_habitat_audit", "_habitat_audit2"}


def convert(text: str) -> tuple[str, int, int]:
    n_disp = 0
    n_inl = 0

    def repl_disp(m: re.Match[str]) -> str:
        nonlocal n_disp
        n_disp += 1
        body = m.group(1)
        if body.startswith("\n"):
            body = body[1:]
        if body.endswith("\n"):
            body = body[:-1]
        # GitHub: blank line optional; keep body clean
        return f"$$\n{body}\n$$"

    def repl_inl(m: re.Match[str]) -> str:
        nonlocal n_inl
        n_inl += 1
        return f"${m.group(1)}$"

    # Display: \[ ... \]
    text = re.sub(r"\\\[(.*?)\\\]", repl_disp, text, flags=re.S)
    # Inline: \( ... \)
    text = re.sub(r"\\\((.*?)\\\)", repl_inl, text, flags=re.S)
    return text, n_disp, n_inl


def main() -> None:
    total = 0
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP for part in path.parts):
            continue
        original = path.read_text(encoding="utf-8")
        if r"\[" not in original and r"\(" not in original:
            continue
        updated, n_disp, n_inl = convert(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            rel = path.relative_to(ROOT)
            print(f"{rel}: display={n_disp} inline={n_inl}")
            total += n_disp + n_inl
    print(f"total replacements: {total}")

    # Sanity: README crown must contain $$
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "$$" in readme and r"\[" not in readme, "README conversion failed"
    i = readme.find("### Flattening")
    print("--- README Flattening sample ---")
    print(readme[i : i + 420])


if __name__ == "__main__":
    main()
