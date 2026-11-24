"""Fortune-cookie entry for make.fun.

Writes one original fortune-cookie line for a software developer to
/output/entry.txt. The house judge reads the file and compares the line
two at a time against the other entries.
"""

import os
from pathlib import Path

FORTUNE = (
    "The feature flag you forgot to remove is still deciding, quietly, "
    "which users meet the future and which meet the past."
)

MAX_CHARS = 120


def validate(line: str) -> str:
    """Return the line if it satisfies the competition gate, else raise."""
    if not isinstance(line, str):
        raise TypeError("entry must be text")
    if len(line) < 1 or len(line) > MAX_CHARS:
        raise ValueError("entry line must be 1-120 characters")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if line != line.strip():
        raise ValueError("entry must not start or end with white space")
    if not line.strip():
        raise ValueError("entry must not be only white space")
    return line


def write_entry(line: str) -> Path:
    """Write the validated line plus a newline to the output file."""
    target_dir = Path(os.environ.get("OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.txt"
    target.write_text(line + "\n", encoding="utf-8", newline="\n")
    return target


def main() -> None:
    line = validate(FORTUNE)
    target = write_entry(line)
    # Read back what was written: a partial or mangled write must fail
    # loudly here instead of shipping a broken entry to the judge.
    if target.read_text(encoding="utf-8") != line + "\n":
        raise RuntimeError("entry.txt does not match the validated line")


if __name__ == "__main__":
    main()
