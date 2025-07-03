#!/usr/bin/env python3
"""
split_sitemap.py – split large sitemap into smaller categorized sitemaps
"""
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone

def split_sitemap(sitemap_path: Path, output_dir: Path):
    """Split the large sitemap into smaller categorized sitemaps"""
    
    # Parse the existing sitemap
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    
    # Define categories
    categories = {
        'rimworld': [],
        'verse': [],
        'unity': [],
        'other': []
    }
    
    # Categorize URLs
    total_urls = 0
    for url_elem in root.findall('.//url'):
        loc_elem = url_elem.find('loc')
        if loc_elem is not None and loc_elem.text is not None:
            url = loc_elem.text
            total_urls += 1
            if 'RimWorld.' in url:
                categories['rimworld'].append(url_elem)
            elif 'Verse.' in url:
                categories['verse'].append(url_elem)
            elif 'Unity' in url:
                categories['unity'].append(url_elem)
            else:
                categories['other'].append(url_elem)
    
    print(f"Total URLs processed: {total_urls}")
    for category, urls in categories.items():
        print(f"{category}: {len(urls)} URLs")
    
    # Create sitemaps for each category
    for category, urls in categories.items():
        if urls:
            create_category_sitemap(category, urls, output_dir)

def create_category_sitemap(category: str, urls: list, output_dir: Path):
    """Create a sitemap for a specific category"""
    NS = {"": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    ET.register_namespace("", NS[""])
    
    urlset = ET.Element("urlset", {"xmlns": NS[""]})
    
    for url_elem in urls:
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = url_elem.text
        ET.SubElement(url, "lastmod").text = "2025-07-03"
    
    # Write the sitemap
    output_path = output_dir / f"sitemap-{category}.xml"
    tree = ET.ElementTree(urlset)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"Created {output_path} with {len(urls)} URLs")

if __name__ == "__main__":
    script_dir = Path(__file__).parent
    sitemap_path = script_dir / "sitemap.xml"
    
    if not sitemap_path.exists():
        print(f"Error: {sitemap_path} does not exist")
        exit(1)
    
    split_sitemap(sitemap_path, script_dir)
    print("Sitemap splitting complete!") 