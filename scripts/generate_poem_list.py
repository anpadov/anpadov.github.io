#!/usr/bin/env python3
import json, pathlib, re

POEMS_DIR = pathlib.Path("poems")
OUT = pathlib.Path("poem-list.json")

PAT_FILE = re.compile(r"poem(\d{10})\.(txt|md)$", re.I)

poems = []

for f in POEMS_DIR.iterdir():
    m = PAT_FILE.match(f.name)
    if not m:
        continue

    timestamp = m.group(1)  # YYYYMMDDHH

    with f.open("r", encoding="utf-8-sig") as fp:
        lines = [l.strip() for l in fp if l.strip()]

    if not lines:
        continue

    title = lines[0]

    poems.append({
        "file": f.as_posix(),
        "title": title,
        "ts": timestamp
    })

# сортировка: новые → старые
poems.sort(key=lambda p: p["ts"], reverse=True)

OUT.write_text(
    json.dumps(poems, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"✅ poem-list.json обновлён ({len(poems)} стихов)")
