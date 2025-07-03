#!/usr/bin/env python3
"""
generate_sitemap.py – create sitemap.xml for a static site
Usage:  python generate_sitemap.py [path/to/site] [https://yoursite.example/]
"""
import sys, xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone

def build_sitemap(site_root: Path, base_url: str) -> bytes:
    NS = {"": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    ET.register_namespace("", NS[""])
    urlset = ET.Element("urlset", {"xmlns": NS[""]})

    for path in sorted(site_root.rglob("*.html")):
        if path.name == "404.html":       # skip utility pages
            continue
        rel = path.relative_to(site_root)
        loc = str(rel.with_suffix("")) if path.name == "index.html" else str(rel)
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = f"{base_url}{loc}"
        mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        ET.SubElement(url, "lastmod").text = mtime.date().isoformat()

    return ET.tostring(urlset, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    # Get arguments with defaults
    if len(sys.argv) >= 2:
        root = Path(sys.argv[1])
    else:
        # Default to the api/ folder within the current script's directory
        script_dir = Path(__file__).parent
        root = script_dir / "api"
    
    if len(sys.argv) >= 3:
        base = sys.argv[2].rstrip("/") + "/"
    else:
        base = "https://pkp24.github.io/RimworldAPI_Docx/"  # Default base URL for RimWorld API
    
    # Validate that the root path exists
    if not root.exists():
        print(f"Error: Path '{root}' does not exist")
        sys.exit(1)
    
    sitemap = build_sitemap(root, base)
    # Generate sitemap in the script's directory (RimworldAPI_Docx root), not in api/
    output_path = Path(__file__).parent / "sitemap.xml"
    output_path.write_bytes(sitemap)
    print(f"Wrote {len(list(root.rglob('*.html')))} URLs → {output_path}")
