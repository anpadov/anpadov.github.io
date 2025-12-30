#!/usr/bin/env python3
import json, pathlib, re

POEMS_DIR = pathlib.Path("poems")
OUT = pathlib.Path("poem-list.json")

PAT_FILE = re.compile(r"^poem(\d{10})\s*(.+?)\.(txt|md)$", re.I)
#            poem YYYYMMDDTT   название

poems = []

for f in POEMS_DIR.iterdir():
    m = PAT_FILE.match(f.name)
    if not m:
        continue

    stamp = m.group(1)      # 2020092902
    raw_title = m.group(2)  # poterya dushi

    year  = stamp[0:4]
    month = stamp[4:6]
    day   = stamp[6:8]

    date = f"{year}-{month}-{day}"

    title = raw_title.replace('_', ' ').strip()

    poems.append({
        "file": f.as_posix(),
        "title": title,
        "date": date,
        "sort": stamp
    })

# сортировка по имени файла (самые новые первые)
poems.sort(key=lambda p: p["sort"], reverse=True)

# поле sort больше не нужно
for p in poems:
    del p["sort"]

OUT.write_text(
    json.dumps(poems, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"✅ poem-list.json обновлён ({len(poems)} стихов)")
