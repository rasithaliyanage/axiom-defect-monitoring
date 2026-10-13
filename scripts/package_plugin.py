#!/usr/bin/env python3
"""Materialise the Claude Code plugin package from the authoritative sources.

Source of truth is `.claude/` — the skills and hook that this repository
actually uses. This script copies them into `plugin/`, which is the installable
package. Nothing is authored in `plugin/skills/` or `plugin/hooks/*.py`.

Why a copy rather than a reference
----------------------------------
The Claude Code plugin model requires a plugin's capabilities to live inside
the plugin root: `skills/<name>/SKILL.md`, `hooks/hooks.json`. There is no
documented mechanism for a plugin to point at files elsewhere in a repository,
and none is invented here. So the package is a mirror, and the mirror is kept
honest mechanically: `tests/plugin/test_plugin_package.py` fails if any copied
file drifts from its source.

This is the same arrangement the repository already uses for
`apps/ui/src/generated/fixtures.ts` — generated, committed, and verified rather
than hand-maintained.

Run from the repository root:
    .venv/Scripts/python.exe scripts/package_plugin.py
    .venv/Scripts/python.exe scripts/package_plugin.py --check    # verify only
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugin"

SKILLS = ("verify-project", "review-uispec", "checkpoint-review")
HOOK = "check_uispec_schema.py"

GENERATED_NOTE = "GENERATED-MIRROR"


def mirrored_files() -> list[tuple[Path, Path]]:
    """Every (source, packaged) pair this script is responsible for."""
    pairs: list[tuple[Path, Path]] = []
    for skill in SKILLS:
        src_dir = ROOT / ".claude" / "skills" / skill
        for src in sorted(src_dir.rglob("*.md")):
            pairs.append((src, PLUGIN / "skills" / skill / src.relative_to(src_dir)))
    pairs.append((ROOT / ".claude" / "hooks" / HOOK, PLUGIN / "hooks" / HOOK))
    return pairs


def check() -> int:
    """Report drift without touching anything. Exit 1 if the package is stale."""
    problems: list[str] = []
    for src, dst in mirrored_files():
        rel = dst.relative_to(ROOT).as_posix()
        if not src.exists():
            problems.append(f"source missing: {src.relative_to(ROOT).as_posix()}")
        elif not dst.exists():
            problems.append(f"not packaged:   {rel}")
        elif not filecmp.cmp(src, dst, shallow=False):
            problems.append(f"drifted:        {rel}")

    # Anything in the mirrored areas that no longer has a source is stale.
    expected = {dst for _, dst in mirrored_files()}
    for area in (PLUGIN / "skills", PLUGIN / "hooks"):
        if not area.exists():
            continue
        for found in area.rglob("*"):
            if found.is_file() and found.name != "hooks.json" and found not in expected:
                problems.append(f"orphaned:       {found.relative_to(ROOT).as_posix()}")

    if problems:
        print("plugin package is out of date:")
        for p in problems:
            print(f"  {p}")
        print("\nRun: .venv/Scripts/python.exe scripts/package_plugin.py")
        return 1

    print(f"plugin package is current ({len(expected)} mirrored files).")
    return 0


def build() -> int:
    copied = 0
    for src, dst in mirrored_files():
        if not src.exists():
            print(f"ERROR source missing: {src}", file=sys.stderr)
            return 1
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        copied += 1
    print(f"packaged {copied} files into {PLUGIN.relative_to(ROOT).as_posix()}/")
    print("plugin/hooks/hooks.json is authored, not mirrored — it is the "
          "plugin-form hook configuration.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="verify the package matches its sources; change nothing")
    args = parser.parse_args()
    return check() if args.check else build()


if __name__ == "__main__":
    raise SystemExit(main())
