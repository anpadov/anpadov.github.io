#!/usr/bin/env python3
import json, pathlib, re

POEMS_DIR = pathlib.Path("poems")
OUT = pathlib.Path("poem-list.json")

PAT_FILE = re.compile(r"\.(txt|md)$", re.I)
PAT_ORDER = re.compile(r"poem(\d{10,14})", re.I)  # poem2020092902

poems = []

for f in POEMS_DIR.iterdir():
    if not PAT_FILE.search(f.name):
        continue

    m = PAT_ORDER.search(f.name)
    if not m:
        continue  # если файл не по формату — пропускаем

    order = m.group(1)

    with f.open("r", encoding="utf-8-sig") as fp:
        lines = [l.rstrip() for l in fp.readlines() if l.strip()]

    if not lines:
        continue

    title = lines[0]  # заголовок ТОЛЬКО из текста

    poems.append({
        "file": f.as_posix(),
        "title": title,
        "order": order
    })

# сортировка: новые сверху
poems.sort(key=lambda p: p["order"], reverse=True)

OUT.write_text(
    json.dumps(poems, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"✅ poem-list.json обновлён ({len(poems)} стихов)")
