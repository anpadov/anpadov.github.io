#!/usr/bin/env python3
import json, pathlib, re

POEMS_DIR = pathlib.Path("poems")
OUT = pathlib.Path("poem-list.json")

PAT = re.compile(
    r"poem(?P<dt>\d{10})_(?P<title>.+)\.(txt|md)$",
    re.I
)

poems = []

for f in POEMS_DIR.iterdir():
    m = PAT.match(f.name)
    if not m:
        continue

    dt = m.group("dt")          # YYYYMMDDHH
    title_raw = m.group("title")

    date = f"{dt[0:4]}-{dt[4:6]}-{dt[6:8]}"
    sort_key = dt               # для сортировки

    title = title_raw.replace("_", " ")

    poems.append({
        "file": f.as_posix(),
        "title": title,
        "date": date,
        "sort": sort_key
    })

poems.sort(key=lambda p: p["sort"], reverse=True)

OUT.write_text(
    json.dumps(poems, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"✅ poem-list.json обновлён ({len(poems)} стихов)")
