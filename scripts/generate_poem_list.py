#!/usr/bin/env python3
import json, pathlib, re

POEMS_DIR = pathlib.Path("poems")
OUT = pathlib.Path("poem-list.json")
PAT_FILE = re.compile(r"\.(txt|md)$", re.I)
PAT_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")

poems = []

for f in sorted(POEMS_DIR.iterdir(), key=lambda p: p.name.lower()):
    if not PAT_FILE.search(f.name):
        continue

    with f.open("r", encoding="utf-8-sig") as fp:  # SIG удаляет BOM!
        lines = [line.strip() for line in fp if line.strip()]

    if not lines:
        print(f"⚠️  Пропущен пустой файл: {f}")
        continue

    title = lines[0]
    date = "1900-01-01"

    if len(lines) >= 2:
        second_line = lines[1]
        if PAT_DATE.fullmatch(second_line):
            date = second_line
        else:
            print(f"⚠️  Невалидная дата во 2-й строке файла {f}: «{second_line}»")
    else:
        print(f"⚠️  Нет второй строки (даты) в {f}")

    poems.append({
        "file": f.as_posix(),
        "title": title,
        "date": date
    })

# Сортировка по дате (свежие выше)
poems.sort(key=lambda p: p["date"], reverse=True)

OUT.write_text(json.dumps(poems, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✅ Список готов: {len(poems)} стихов")
