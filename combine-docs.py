#!/usr/bin/env python3
"""
combine-docs.py – Combine related HTML documentation pages into fewer, comprehensive pages
to reduce the total number of files for better crawling.
"""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
import html

API_DIR = Path(__file__).parent / "api"
FILE_LIST = API_DIR / "file-list.json"
OUTPUT_DIR = Path(__file__).parent / "combined-docs"

# Create output directory
OUTPUT_DIR.mkdir(exist_ok=True)

def load_file_list():
    """Load the file list with namespace information"""
    with open(FILE_LIST, encoding="utf-8-sig") as f:
        return json.load(f)

def extract_content_from_html(file_path):
    """Extract the main content from an HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the main content area - look for the article with content class
        content = soup.find('article', class_='content wrap')
        
        if content:
            # Remove navigation, headers, footers, etc.
            for unwanted in content.find_all(['nav', 'header', 'footer', 'script', 'style']):
                unwanted.decompose()
            
            return str(content)
        else:
            return ""
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def group_files_by_category(files):
    """Group files into logical categories for combining"""
    categories = {
        'RimWorld_Alerts': [],
        'RimWorld_Buildings': [],
        'RimWorld_Combat': [],
        'RimWorld_AI': [],
        'RimWorld_Items': [],
        'RimWorld_Characters': [],
        'RimWorld_World': [],
        'RimWorld_UI': [],
        'Verse_Core': [],
        'Verse_Graphics': [],
        'Verse_Utilities': [],
        'Unity_Core': [],
        'Unity_Graphics': [],
        'Unity_Input': [],
        'Unity_Physics': [],
        'Unity_Audio': [],
        'Other_Libraries': []
    }
    
    for file_info in files:
        name = file_info['name'].replace('.html', '')
        namespace = file_info.get('namespace', '')
        path = file_info['path']
        
        # Categorize based on namespace and name patterns
        if namespace.startswith('RimWorld.'):
            if 'Alert' in name or 'Alert' in namespace:
                categories['RimWorld_Alerts'].append(file_info)
            elif 'Building' in name or 'Building' in namespace:
                categories['RimWorld_Buildings'].append(file_info)
            elif any(word in name for word in ['Weapon', 'Combat', 'Attack', 'Defense', 'Turret', 'Trap']):
                categories['RimWorld_Combat'].append(file_info)
            elif any(word in name for word in ['AI', 'Job', 'Work', 'Think', 'Behavior']):
                categories['RimWorld_AI'].append(file_info)
            elif any(word in name for word in ['Thing', 'Item', 'Apparel', 'Weapon', 'Food']):
                categories['RimWorld_Items'].append(file_info)
            elif any(word in name for word in ['Pawn', 'Character', 'Human', 'Animal', 'Race']):
                categories['RimWorld_Characters'].append(file_info)
            elif any(word in name for word in ['World', 'Map', 'Tile', 'Biome', 'Weather']):
                categories['RimWorld_World'].append(file_info)
            elif any(word in name for word in ['UI', 'Window', 'Dialog', 'Widget', 'Button']):
                categories['RimWorld_UI'].append(file_info)
            else:
                categories['RimWorld_Alerts'].append(file_info)  # Default for RimWorld
        elif namespace.startswith('Verse.'):
            if any(word in name for word in ['Thing', 'Def', 'Comp', 'Root']):
                categories['Verse_Core'].append(file_info)
            elif any(word in name for word in ['Graphic', 'Draw', 'Render', 'Texture', 'Material']):
                categories['Verse_Graphics'].append(file_info)
            else:
                categories['Verse_Utilities'].append(file_info)
        elif namespace.startswith('UnityEngine.'):
            if any(word in name for word in ['Object', 'Component', 'GameObject', 'Transform']):
                categories['Unity_Core'].append(file_info)
            elif any(word in name for word in ['Render', 'Texture', 'Material', 'Shader', 'Mesh']):
                categories['Unity_Graphics'].append(file_info)
            elif any(word in name for word in ['Input', 'Key', 'Mouse', 'Touch']):
                categories['Unity_Input'].append(file_info)
            elif any(word in name for word in ['Physics', 'Collider', 'Rigidbody', 'Raycast']):
                categories['Unity_Physics'].append(file_info)
            elif any(word in name for word in ['Audio', 'Sound', 'Clip', 'Source']):
                categories['Unity_Audio'].append(file_info)
            else:
                categories['Unity_Core'].append(file_info)
        else:
            categories['Other_Libraries'].append(file_info)
    
    return categories

def create_combined_html(category_name, files, output_path):
    """Create a combined HTML file for a category"""
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category_name} - Combined API Documentation</title>
    <meta name="robots" content="index, follow">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        .toc {{ background: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        .toc h2 {{ margin-top: 0; color: #34495e; }}
        .toc ul {{ list-style: none; padding: 0; }}
        .toc li {{ margin: 5px 0; }}
        .toc a {{ color: #2980b9; text-decoration: none; font-weight: 500; }}
        .toc a:hover {{ text-decoration: underline; }}
        .section {{ margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
        .section h3 {{ color: #e74c3c; margin-top: 0; }}
        .section-content {{ margin-top: 15px; }}
        .back-to-top {{ position: fixed; bottom: 20px; right: 20px; background: #3498db; color: white; padding: 10px 15px; border-radius: 5px; text-decoration: none; }}
        .back-to-top:hover {{ background: #2980b9; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{category_name} - Combined API Documentation</h1>
        <p>This page contains combined documentation for {len(files)} related API classes and components.</p>
        
        <div class="toc">
            <h2>Table of Contents</h2>
            <ul>
"""
    
    # Add table of contents
    for i, file_info in enumerate(files):
        name = file_info['name'].replace('.html', '')
        html_content += f'                <li><a href="#section-{i}">{name}</a></li>\n'
    
    html_content += """            </ul>
        </div>
"""
    
    # Add content sections
    for i, file_info in enumerate(files):
        name = file_info['name'].replace('.html', '')
        namespace = file_info.get('namespace', '')
        # The path in file_info already includes 'api/', so we need to construct it relative to the script location
        original_path = Path(__file__).parent / file_info['path']
        
        html_content += f"""
        <div class="section" id="section-{i}">
            <h3>{name}</h3>
            <p><strong>Namespace:</strong> {namespace}</p>
            <div class="section-content">
"""
        
        # Extract and add content from original file
        content = extract_content_from_html(original_path)
        if content:
            # Clean up the content
            content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
            content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
            html_content += content
        else:
            html_content += f'<p>Content not available for {name}</p>'
        
        html_content += """
            </div>
        </div>
"""
    
    html_content += """
    </div>
    <a href="#" class="back-to-top">↑ Top</a>
</body>
</html>"""
    
    # Write the combined file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Created {output_path} with {len(files)} combined pages")

def main():
    """Main function to combine documentation files"""
    print("Loading file list...")
    files = load_file_list()
    
    print("Grouping files by category...")
    categories = group_files_by_category(files)
    
    print("Creating combined documentation files...")
    combined_files = []
    
    for category_name, category_files in categories.items():
        if category_files:
            output_path = OUTPUT_DIR / f"{category_name}.html"
            create_combined_html(category_name, category_files, output_path)
            combined_files.append({
                'name': f"{category_name}.html",
                'path': str(output_path.relative_to(Path(__file__).parent)),
                'count': len(category_files)
            })
    
    # Create index file for combined docs
    index_path = OUTPUT_DIR / "index.html"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Combined RimWorld API Documentation</title>
    <meta name="robots" content="index, follow">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; text-align: center; }}
        .category {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .category h3 {{ margin-top: 0; color: #e74c3c; }}
        .category a {{ color: #2980b9; text-decoration: none; font-weight: bold; }}
        .category a:hover {{ text-decoration: underline; }}
        .count {{ color: #7f8c8d; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Combined RimWorld API Documentation</h1>
        <p>This index contains {len(combined_files)} combined documentation files covering {sum(f['count'] for f in combined_files)} individual API classes.</p>
""")
        
        for file_info in combined_files:
            f.write(f"""
        <div class="category">
            <h3><a href="{file_info['name']}">{file_info['name'].replace('.html', '')}</a></h3>
            <p class="count">Contains {file_info['count']} API classes</p>
        </div>
""")
        
        f.write("""
    </div>
</body>
</html>""")
    
    print(f"\nCombined documentation created in {OUTPUT_DIR}")
    print(f"Total files: {len(combined_files)} (down from {len(files)})")
    print(f"Reduction: {((len(files) - len(combined_files)) / len(files) * 100):.1f}%")
    print(f"\nIndex file: {index_path}")

if __name__ == "__main__":
    main() 