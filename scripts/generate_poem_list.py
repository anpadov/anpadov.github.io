#!/usr/bin/env python3
import json, pathlib, re

POEMS_DIR = pathlib.Path("poems")
OUT       = pathlib.Path("poem-list.json")
PAT_FILE  = re.compile(r"\.(txt|md)$", re.I)
PAT_DATE  = re.compile(r"\d{4}-\d{2}-\d{2}")

poems = []

for f in sorted(POEMS_DIR.iterdir(), key=lambda p: p.name.lower()):
    if not PAT_FILE.search(f.name):
        continue

    with f.open("r", encoding="utf-8-sig") as fp:        # utf‑8‑sig убирает BOM
        raw_lines = fp.readlines()

    # убираем пустые строки в начале
    lines = [l.strip() for l in raw_lines if l.strip()]
    if not lines:
        continue

    title_line = lines[0]
    date = "1900-01-01"
    title = title_line

    # 1) ищем дату прямо в заголовке
    m = PAT_DATE.search(title_line)
    if m:
        date = m.group()
        title = title_line[:m.start()].strip()
    # 2) если не нашли — проверяем вторую строку
    elif len(lines) > 1 and PAT_DATE.fullmatch(lines[1]):
        date = lines[1]

    poems.append({
        "file": f.as_posix(),
        "title": title,
        "date":  date
    })

poems.sort(key=lambda p: p["date"], reverse=True)
OUT.write_text(json.dumps(poems, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✅ poem-list.json обновлён ({len(poems)} стихов)")
