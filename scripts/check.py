#!/usr/bin/env python3
"""Sanity checks for the published files. Exits non-zero on any failure.

- every SVG is well-formed XML with the expected viewBox and accessible label
- every SVG stays under the size budget
- only the free motion (drop) and the static frame ship in this repository
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUDGET = 1600  # bytes per SVG
SHAPES = "iotszjl"
# Motions that belong to the commercial pack and must never be published here.
EXCLUDED = ["spin", "turn", "wobble", "@keyframes s{", "@keyframes t{", "@keyframes w{"]
# Text that must not appear anywhere in the published tree.
BANNED_WORDS = re.compile("te" + "tris", re.I)
# Only compositor-friendly properties may be animated.
ALLOWED_PROPS = {"transform", "opacity", "animation-timing-function"}


def keyframe_props(css):
    """Yield every property name declared inside @keyframes blocks."""
    for m in re.finditer(r"@keyframes\s*[\w-]+\s*\{", css):
        depth, i = 1, m.end()
        while depth and i < len(css):
            depth += {"{": 1, "}": -1}.get(css[i], 0)
            i += 1
        body = css[m.end():i - 1]
        yield from re.findall(r"([a-z-]+)\s*:", re.sub(r"[\d.,% ]+\{", "{", body))

errors = []
for k in SHAPES:
    p = ROOT / "svg" / f"tetromino-{k}.svg"
    if not p.exists():
        errors.append(f"missing {p.name}")
        continue
    text = p.read_text()
    try:
        root = ET.fromstring(text)
    except ET.ParseError as e:
        errors.append(f"{p.name}: invalid XML ({e})")
        continue
    if root.get("viewBox") != "0 0 32 32":
        errors.append(f"{p.name}: unexpected viewBox {root.get('viewBox')!r}")
    if root.get("role") != "img" or not root.get("aria-label"):
        errors.append(f"{p.name}: missing role/aria-label")
    if len(text.encode()) > BUDGET:
        errors.append(f"{p.name}: {len(text.encode())} B exceeds {BUDGET} B budget")
    bad = set(keyframe_props(text)) - ALLOWED_PROPS
    if bad:
        errors.append(f"{p.name}: animates non-compositor properties {sorted(bad)}")
    for word in EXCLUDED:
        if word in text:
            errors.append(f"{p.name}: contains excluded motion {word!r}")

for p in ROOT.rglob("*"):
    if p.is_file() and ".git" not in p.parts and p.suffix in {".svg", ".js", ".ts", ".html", ".md", ".json", ".py", ".yml", ""}:
        if BANNED_WORDS.search(p.read_text(errors="ignore")):
            errors.append(f"{p.relative_to(ROOT)}: contains a banned word")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"ok: {len(SHAPES)} shapes checked")
