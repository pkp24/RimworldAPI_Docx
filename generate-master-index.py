#!/usr/bin/env python3
"""
generate-master-index.py – Generate a static HTML index page with links to all API docs, grouped by namespace.
"""
import json
from pathlib import Path

API_DIR = Path(__file__).parent / "api"
FILE_LIST = API_DIR / "file-list.json"
OUTPUT = Path(__file__).parent / "all-docs.html"

# Load file list
with open(FILE_LIST, encoding="utf-8-sig") as f:
    files = json.load(f)

# Group by namespace
namespaces = {}
for entry in files:
    ns = entry.get("namespace", "(none)")
    namespaces.setdefault(ns, []).append(entry)

# Sort namespaces and files
sorted_ns = sorted(namespaces.keys())
for ns in sorted_ns:
    namespaces[ns].sort(key=lambda e: e["name"])

# Generate HTML
with open(OUTPUT, "w", encoding="utf-8") as out:
    out.write("""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <title>All RimWorld API Docs</title>
    <meta name=\"robots\" content=\"index, follow\">
    <style>
        body { font-family: sans-serif; background: #f8f9fa; color: #222; }
        h1 { text-align: center; }
        .namespace { margin: 2em 0 1em 0; font-size: 1.3em; color: #4a4a8a; }
        ul { columns: 3 300px; -webkit-columns: 3 300px; -moz-columns: 3 300px; }
        li { margin-bottom: 0.2em; }
        a { color: #2a4a8a; text-decoration: none; }
        a:hover { text-decoration: underline; color: #667eea; }
        @media (max-width: 900px) { ul { columns: 2 200px; } }
        @media (max-width: 600px) { ul { columns: 1 100px; } }
    </style>
</head>
<body>
    <h1>All RimWorld API Documentation</h1>
    <p style=\"text-align:center;\">Links to every API doc page, grouped by namespace.</p>
""")
    for ns in sorted_ns:
        out.write(f'<div class="namespace">{ns}</div>\n<ul>\n')
        for entry in namespaces[ns]:
            name = entry["name"].replace('.html', '')
            path = entry["path"]
            out.write(f'  <li><a href="{path}" target="_blank">{name}</a></li>\n')
        out.write('</ul>\n')
    out.write("""
</body>
</html>
""")
print(f"Wrote {OUTPUT} with {len(files)} links.") 