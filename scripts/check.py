#!/usr/bin/env python3
# Author: spicyzhug@gmail.com
# Copyright (c) 2026 lituus-io. All rights reserved.
# Licensed under the MIT License (see LICENSE).
"""Sanity checks for the published files. Exits non-zero on any failure.

- every SVG is well-formed XML with the expected viewBox and accessible label
- every SVG stays under its size budget
- only the free animations ship here: drop and the static frame, plus the five
  motion loops in svg/motion/ (spin, turn, wobble, squash, melt)
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUDGET = 1600         # bytes per drop SVG
MOTION_BUDGET = 3072  # bytes per motion SVG
SHAPES = "iotszjl"
MOTIONS = ["spin", "turn", "wobble", "squash", "melt"]
# Animations that belong to the commercial pack and must never be published here.
EXCLUDED = ["dance", "shimmy", "twist", "robot", "disco", "hop-step", "spin-out", "wave-through",
            "assemble", "conga", "lottie"]
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

FILES = [(ROOT / "svg" / f"tetromino-{k}.svg", BUDGET) for k in SHAPES]
FILES += [(ROOT / "svg" / "motion" / f"tetromino-{k}-{m}.svg", MOTION_BUDGET) for m in MOTIONS for k in SHAPES]

errors = []
extra = {p for p in (ROOT / "svg").rglob("*.svg")} - {p for p, _ in FILES}
errors += [f"unexpected file {p.relative_to(ROOT)}" for p in sorted(extra)]
for p, budget in FILES:
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
    if len(text.encode()) > budget:
        errors.append(f"{p.name}: {len(text.encode())} B exceeds {budget} B budget")
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
print(f"ok: {len(FILES)} SVGs checked ({len(SHAPES)} shapes, {len(MOTIONS)} motions)")
