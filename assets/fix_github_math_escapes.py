"""Fix LaTeX inside GitHub Markdown math so GFM does not eat backslashes.

GFM treats \\ before ASCII punctuation as an escape, so before MathJax runs:
  \\{  ->  {
  \\,  ->  ,
  \\;  ->  ;
which breaks \\Bigl\\{, thin spaces, etc.

Strategy (safe for already-correct files):
  - Inside $...$ and $$...$$, double a backslash when it precedes
    markdown-escapable punctuation that LaTeX also uses as a command char.

Run: python assets/fix_github_math_escapes.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "__pycache__", ".pytest_cache"}

# CommonMark escapable ASCII punctuation that also appears in LaTeX cmds
# After GFM: \\X -> X, so we need \\\\X in the source to leave \\X for MathJax.
PUNCT = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")


def protect_math_segment(seg: str) -> str:
    """Double backslash before escapable punctuation (if not already doubled)."""
    out: list[str] = []
    i = 0
    n = len(seg)
    while i < n:
        ch = seg[i]
        if ch == "\\" and i + 1 < n:
            nxt = seg[i + 1]
            # already doubled (\\{ style): keep one pair, don't triple
            if nxt == "\\" and i + 2 < n and seg[i + 2] in PUNCT:
                out.append(seg[i : i + 3])
                i += 3
                continue
            if nxt in PUNCT:
                # \{ -> \\{  so GFM leaves \{
                out.append("\\\\")
                out.append(nxt)
                i += 2
                continue
        out.append(ch)
        i += 1
    return "".join(out)


def protect_file(text: str) -> str:
    # display $$...$$ first
    def repl_disp(m: re.Match[str]) -> str:
        return "$$" + protect_math_segment(m.group(1)) + "$$"

    text = re.sub(r"\$\$(.*?)\$\$", repl_disp, text, flags=re.S)

    # inline $...$ (not $$)
    def repl_inl(m: re.Match[str]) -> str:
        return "$" + protect_math_segment(m.group(1)) + "$"

    text = re.sub(r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)", repl_inl, text, flags=re.S)
    return text


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*.md")):
        if any(p in SKIP for p in path.parts):
            continue
        original = path.read_text(encoding="utf-8")
        if "$" not in original:
            continue
        updated = protect_file(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            print(path.relative_to(ROOT))
            changed += 1
    print(f"files updated: {changed}")

    # show the gain-sensitive block
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    i = readme.find("Gain-sensitive")
    print("--- sample ---")
    print(readme[i : i + 380])


if __name__ == "__main__":
    main()
