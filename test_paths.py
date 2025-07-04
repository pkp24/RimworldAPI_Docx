#!/usr/bin/env python3
import json
from pathlib import Path
from bs4 import BeautifulSoup

# Load file list
with open('api/file-list.json', encoding='utf-8-sig') as f:
    files = json.load(f)

# Test with first few RimWorld files
rimworld_files = [f for f in files if f.get('namespace', '').startswith('RimWorld.')][:3]

for file_info in rimworld_files:
    name = file_info['name']
    path = file_info['path']
    
    # Construct path the same way as the main script
    file_path = Path(__file__).parent / path
    
    print(f"\nTesting: {name}")
    print(f"Path from JSON: {path}")
    print(f"Constructed path: {file_path}")
    print(f"File exists: {file_path.exists()}")
    
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            article = soup.find('article', class_='content wrap')
            
            if article:
                print(f"✓ Found article, length: {len(str(article))}")
                # Remove unwanted elements
                for unwanted in article.find_all(['nav', 'header', 'footer', 'script', 'style']):
                    unwanted.decompose()
                print(f"✓ After cleanup, length: {len(str(article))}")
            else:
                print("✗ No article found")
        except Exception as e:
            print(f"✗ Error: {e}")
    else:
        print("✗ File not found") 