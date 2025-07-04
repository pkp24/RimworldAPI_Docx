#!/usr/bin/env python3
"""
generate-master-index.py – Generate a static HTML index page with links to all API docs, grouped by namespace.
Also generates split sitemaps (one per DLL) and a sitemap-index.xml referencing them.
"""
import json
import re
from pathlib import Path

API_DIR = Path(__file__).parent / "api"
FILE_LIST = API_DIR / "file-list.json"
OUTPUT = Path(__file__).parent / "all-docs.html"
SITEMAP_INDEX = Path(__file__).parent / "sitemap-index.xml"
SITEMAP_TEMPLATE = "sitemap-{}.xml"
BASE_URL = "https://pkp24.github.io/RimworldAPI_Docx/"

# Load file list
with open(FILE_LIST, encoding="utf-8-sig") as f:
    files = json.load(f)

# Group by DLL (first part of namespace)
dlls = {}
for entry in files:
    ns = entry.get("namespace", "(none)")
    # Extract DLL name from namespace (e.g., "RimWorld" from "RimWorld.Alert")
    dll = ns.split('.')[0] if '.' in ns else ns
    dlls.setdefault(dll, []).append(entry)

# Sort DLLs and files
sorted_dlls = sorted(dlls.keys())
for dll in sorted_dlls:
    dlls[dll].sort(key=lambda e: e["name"])

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
        .dll { margin: 2em 0 1em 0; font-size: 1.3em; color: #4a4a8a; }
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
    <p style=\"text-align:center;\">Links to every API doc page, grouped by DLL.</p>
""")
    for dll in sorted_dlls:
        out.write(f'<div class="dll">{dll}</div>\n<ul>\n')
        for entry in dlls[dll]:
            name = entry["name"].replace('.html', '')
            path = entry["path"]
            out.write(f'  <li><a href="{path}" target="_blank">{name}</a></li>\n')
        out.write('</ul>\n')
    out.write("""
</body>
</html>
""")
print(f"Wrote {OUTPUT} with {len(files)} links.")

# Generate split sitemaps
sitemap_files = []
def safe_dll(dll):
    return re.sub(r'[^A-Za-z0-9]+', '_', dll)

for dll in sorted_dlls:
    sitemap_name = SITEMAP_TEMPLATE.format(safe_dll(dll))
    sitemap_path = Path(__file__).parent / sitemap_name
    sitemap_files.append(sitemap_name)
    with open(sitemap_path, "w", encoding="utf-8") as sm:
        sm.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        sm.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for entry in dlls[dll]:
            url = BASE_URL + entry["path"]
            sm.write(f'  <url><loc>{url}</loc></url>\n')
        sm.write('</urlset>\n')
    print(f"Wrote {sitemap_path} with {len(dlls[dll])} URLs.")

# Generate sitemap-index.xml
with open(SITEMAP_INDEX, "w", encoding="utf-8") as idx:
    idx.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    idx.write('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for sitemap_name in sitemap_files:
        idx.write(f'  <sitemap><loc>{BASE_URL}{sitemap_name}</loc></sitemap>\n')
    idx.write('</sitemapindex>\n')
print(f"Wrote {SITEMAP_INDEX} with {len(sitemap_files)} sitemaps.") 