#!/usr/bin/env python3
import json, pathlib, re, sys

POEMS_DIR = pathlib.Path("poems")
OUT_FILE  = pathlib.Path("poem-list.json")
PATTERN   = re.compile(r"\.(txt|md)$", re.I)

poems = []
for f in sorted(POEMS_DIR.iterdir(), key=lambda p: p.name.lower()):
    if PATTERN.search(f.name):
        # читаем первую непустую строку как заголовок
        with f.open("r", encoding="utf-8") as fp:
            for line in fp:
                title = line.strip()
                if title:
                    poems.append({"file": str(f).replace("\\", "/"), "title": title})
                    break

OUT_FILE.write_text(json.dumps(poems, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✅  {OUT_FILE} обновлён ({len(poems)} стихов).")
