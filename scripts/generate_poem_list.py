#!/usr/bin/env python3
import json, pathlib, re

POEMS_DIR = pathlib.Path("poems")
OUT = pathlib.Path("poem-list.json")
PAT_FILE = re.compile(r"\.(txt|md)$", re.I)
PAT_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")  # строгое совпадение

poems = []

for f in sorted(POEMS_DIR.iterdir(), key=lambda p: p.name.lower()):
    if not PAT_FILE.search(f.name):
        continue

    with f.open("r", encoding="utf-8") as fp:
        lines = [line.strip() for line in fp if line.strip()]

    if len(lines) < 2:
        continue

    title = lines[0]
    date = lines[1] if PAT_DATE.match(lines[1]) else "1900-01-01"

    poems.append({
        "file": f.as_posix(),
        "title": title,
        "date": date
    })

# Сортировка от новых к старым
poems.sort(key=lambda x: x["date"], reverse=True)

OUT.write_text(json.dumps(poems, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✅ poem-list.json создан ({len(poems)} стихов)")
