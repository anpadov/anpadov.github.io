#!/usr/bin/env python3
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = ROOT / "liked-poems"
OUT  = ROOT / "liked-list.json"

print("BASE =", BASE)

items = []

for f in BASE.rglob("*.txt"):
    print("FOUND:", f)
    with f.open(encoding="utf-8-sig") as fp:
        lines = [l.strip() for l in fp if l.strip()]

    if len(lines) < 3:
        print("SKIP (too short):", f)
        continue

    items.append({
        "title": lines[0],
        "author": lines[1],
        "file": f.relative_to(ROOT).as_posix()
    })

OUT.write_text(
    json.dumps(items, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"✅ liked-list.json обновлён ({len(items)} стихов)")
