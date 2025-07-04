#!/usr/bin/env python3
"""
generate-filtered-index.py – Generate an index page for combined documentation files,
excluding the largest RimWorld files for better performance.
"""
import os
from pathlib import Path

COMBINED_DIR = Path(__file__).parent / "combined-docs"
OUTPUT_FILE = Path(__file__).parent / "filtered-index.html"

# Files to exclude (the largest ones)
EXCLUDED_FILES = {
    "RimWorld_Characters.html",
    "RimWorld_World.html", 
    "RimWorld_AI.html"
}

def get_file_info(file_path):
    """Get file size and line count for display"""
    try:
        size = file_path.stat().st_size
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = len(f.readlines())
        
        # Format size
        if size > 1024 * 1024:
            size_str = f"{size / (1024 * 1024):.1f} MB"
        else:
            size_str = f"{size / 1024:.1f} KB"
            
        return size_str, lines
    except Exception as e:
        return "Error", 0

def generate_index():
    """Generate the filtered index HTML"""
    
    # Get all HTML files in combined-docs, excluding the specified ones
    html_files = []
    for file_path in COMBINED_DIR.glob("*.html"):
        if file_path.name not in EXCLUDED_FILES:
            size_str, lines = get_file_info(file_path)
            html_files.append({
                'name': file_path.name,
                'path': file_path.name,
                'size': size_str,
                'lines': lines
            })
    
    # Sort by name
    html_files.sort(key=lambda x: x['name'])
    
    # Generate HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Filtered RimWorld API Documentation Index</title>
    <meta name="description" content="Combined RimWorld API documentation index (excluding largest files for better performance)">
    <meta name="keywords" content="RimWorld, API, documentation, modding, Unity, C#">
    <meta name="robots" content="index, follow">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f8f9fa;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        .info {{
            background: #e8f4fd;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
            border-left: 4px solid #3498db;
        }}
        .file-list {{
            display: grid;
            gap: 15px;
        }}
        .file-item {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e9ecef;
            transition: all 0.3s ease;
        }}
        .file-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-color: #3498db;
        }}
        .file-name {{
            font-size: 1.2em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .file-name a {{
            color: #2980b9;
            text-decoration: none;
        }}
        .file-name a:hover {{
            text-decoration: underline;
        }}
        .file-stats {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .excluded-note {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            color: #856404;
        }}
        .back-link {{
            display: inline-block;
            margin-top: 20px;
            color: #3498db;
            text-decoration: none;
            font-weight: 500;
        }}
        .back-link:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Filtered RimWorld API Documentation Index</h1>
        
        <div class="info">
            <h3>📚 Combined Documentation Files</h3>
            <p>This index contains {len(html_files)} combined documentation files, with the largest files excluded for better performance.</p>
            <p><strong>Total files:</strong> {len(html_files)} combined files (down from 12,527 individual files)</p>
        </div>

        <div class="file-list">
"""

    # Add each file to the HTML
    for file_info in html_files:
        html_content += f"""            <div class="file-item">
                <div class="file-name">
                    <a href="combined-docs/{file_info['path']}" target="_blank">
                        {file_info['name']}
                    </a>
                </div>
                <div class="file-stats">
                    📄 {file_info['size']} • 📝 {file_info['lines']:,} lines
                </div>
            </div>
"""

    # Add excluded files note
    html_content += f"""        </div>

        <div class="excluded-note">
            <h4>⚠️ Excluded Files</h4>
            <p>The following large files were excluded from this index for better performance:</p>
            <ul>
                <li><strong>RimWorld_Characters.html</strong> - Character and pawn-related classes</li>
                <li><strong>RimWorld_World.html</strong> - World generation and management</li>
                <li><strong>RimWorld_AI.html</strong> - AI and behavior systems</li>
            </ul>
            <p>These files can be accessed directly from the <a href="combined-docs/index.html">full combined index</a> if needed.</p>
        </div>

        <a href="combined-docs/index.html" class="back-link">← View Full Combined Index (All Files)</a>
    </div>
</body>
</html>"""

    # Write the file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated filtered index: {OUTPUT_FILE}")
    print(f"Included files: {len(html_files)}")
    print(f"Excluded files: {len(EXCLUDED_FILES)}")
    
    # Show file list
    print("\nIncluded files:")
    for file_info in html_files:
        print(f"  • {file_info['name']} ({file_info['size']}, {file_info['lines']:,} lines)")

if __name__ == "__main__":
    generate_index() 