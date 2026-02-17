#!/usr/bin/env python3
import json, pathlib

BASE = pathlib.Path("liked-poems")
OUT  = pathlib.Path("liked-list.json")

items = []

for f in BASE.rglob("*.txt"):
    with f.open(encoding="utf-8-sig") as fp:
        lines = [l.strip() for l in fp if l.strip()]

    if len(lines) < 3:
        continue

    title  = lines[0]
    author = lines[1]

    items.append({
        "author": author,
        "title": title,
        "file": f.as_posix()
    })

OUT.write_text(
    json.dumps(items, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"✅ liked-list.json обновлён ({len(items)} стихов)")
