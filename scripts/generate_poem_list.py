#!/usr/bin/env python3
import json, pathlib, re, datetime as dt

POEMS_DIR = pathlib.Path("poems")
OUT       = pathlib.Path("poem-list.json")
PAT_FILE  = re.compile(r"\.(txt|md)$", re.I)
PAT_DATE  = re.compile(r"\d{4}-\d{2}-\d{2}")  # YYYY-MM-DD

poems = []

for f in POEMS_DIR.iterdir():
    if not PAT_FILE.search(f.name):
        continue

    title = date = ""
    with f.open("r", encoding="utf-8") as fp:
        lines = [l.rstrip("\n") for l in fp if l.strip()]
    if not lines:
        continue

    title = lines[0].strip()
    # ищем дату во 2‑й строке
    if len(lines) > 1 and PAT_DATE.fullmatch(lines[1].strip()):
        date = lines[1].strip()

    # если даты нет — вместо неё ставим 1900‑01‑01, чтобы ушли в конец
    date_iso = date or "1900-01-01"

    poems.append({
        "file": f.as_posix(),
        "title": title,
        "date":  date_iso
    })

# сортируем по дате DESC (свежее выше)
poems.sort(key=lambda p: p["date"], reverse=True)

OUT.write_text(json.dumps(poems, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✅  {OUT} updated ({len(poems)} poems, newest first)")
