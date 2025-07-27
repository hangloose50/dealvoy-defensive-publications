#!/usr/bin/env python3
"""
Clean USPTO PDF Generator for Dealvoy Patent Application
Creates submission-ready HTML files (convert to PDF manually)
"""

import os
from pathlib import Path

def create_clean_html(title, content, filename):
    """Create clean HTML file for USPTO submission"""
    
    html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ 
            font-family: Times, serif; 
            line-height: 1.6; 
            margin: 1in; 
            font-size: 12pt;
            color: #000;
        }}
        h1 {{ 
            color: #000; 
            border-bottom: 2px solid #000; 
            font-size: 18pt;
            margin-top: 0;
        }}
        h2 {{ 
            color: #000; 
            border-bottom: 1px solid #000; 
            font-size: 14pt;
        }}
        h3 {{ 
            color: #000; 
            font-size: 12pt;
            font-weight: bold;
        }}
        h4 {{ 
            color: #000; 
            font-size: 12pt;
            font-weight: bold;
        }}
        p {{ margin: 6pt 0; }}
        li {{ margin: 3pt 0; }}
        pre {{ 
            background-color: #f9f9f9; 
            padding: 10px; 
            border: 1px solid #ccc;
            font-family: monospace;
            font-size: 10pt;
            page-break-inside: avoid;
        }}
        .page-break {{ page-break-before: always; }}
        .claim {{ 
            margin: 12pt 0;
            padding: 6pt;
            border-left: 3px solid #ccc;
        }}
        @media print {{
            body {{ margin: 0.75in; }}
            .page-break {{ page-break-before: always; }}
        }}
    </style>
</head>
<body>
{content}
</body>
</html>"""
    
    # Save to DEALVOY_USPTO_FILING folder
    output_dir = Path("DEALVOY_USPTO_FILING")
    output_file = output_dir / filename
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"✅ Created: {output_file}")

def clean_markdown_to_html(md_content):
    """Convert markdown to clean HTML for USPTO submission"""
    lines = md_content.split('\n')
    html_content = ""
    in_code_block = False
    
    for line in lines:
        # Skip conversation markers and unnecessary content
        if any(skip in line.lower() for skip in ['conversation', 'chat', '🎯', '⚡', 'ready to file']):
            continue
            
        if line.startswith('```'):
            if in_code_block:
                html_content += '</pre>\n'
                in_code_block = False
            else:
                html_content += '<pre>\n'
                in_code_block = True
            continue
            
        if in_code_block:
            html_content += line + '\n'
            continue
            
        # Headers
        if line.startswith('# '):
            html_content += f'<h1>{line[2:].strip()}</h1>\n'
        elif line.startswith('## '):
            html_content += f'<h2>{line[3:].strip()}</h2>\n'
        elif line.startswith('### '):
            html_content += f'<h3>{line[4:].strip()}</h3>\n'
        elif line.startswith('#### '):
            html_content += f'<h4>{line[5:].strip()}</h4>\n'
        # Claims
        elif line.startswith('**CLAIM'):
            html_content += f'<div class="claim"><h4>{line.replace("**", "").strip()}</h4>'
        elif line.strip() and not line.startswith('---') and not line.startswith('*'):
            # Regular content
            clean_line = line.replace('**', '<strong>').replace('**', '</strong>')
            if line.startswith('- '):
                html_content += f'<li>{clean_line[2:]}</li>\n'
            else:
                html_content += f'<p>{clean_line}</p>\n'
        elif line.strip() == '':
            html_content += '<br>\n'
    
    return html_content

def main():
    """Generate clean USPTO submission files"""
    print("🔄 Creating Clean USPTO Submission Package...")
    print("=" * 50)
    
    # Read the patent application
    with open('USPTO_PATENT_APPLICATION_FINAL.md', 'r', encoding='utf-8') as f:
        patent_content = f.read()
    
    # Read technical diagrams  
    with open('PATENT_DIAGRAMS.md', 'r', encoding='utf-8') as f:
        diagrams_content = f.read()
    
    # Read cover page
    with open('USPTO_COVER_PAGE.md', 'r', encoding='utf-8') as f:
        cover_content = f.read()
    
    # Create the three clean submission files
    create_clean_html(
        "Patent Application Specification",
        clean_markdown_to_html(patent_content),
        "1_Patent_Application_Specification.html"
    )
    
    create_clean_html(
        "Patent Technical Diagrams", 
        clean_markdown_to_html(diagrams_content),
        "2_Patent_Technical_Diagrams.html"
    )
    
    create_clean_html(
        "Patent Cover Page and Forms",
        clean_markdown_to_html(cover_content), 
        "3_Patent_Cover_Page_Forms.html"
    )
    
    print()
    print("🎉 CLEAN USPTO PACKAGE READY!")
    print("=" * 50)
    print("📁 Location: DEALVOY_USPTO_FILING/")
    print()
    print("📋 CONVERT TO PDF:")
    print("1️⃣ Open each HTML file in Chrome/Safari")
    print("2️⃣ Press Cmd+P → Save as PDF")
    print("3️⃣ Upload PDFs to USPTO.gov")
    print()
    print("💰 FILING: $400 (Micro Entity)")
    print("🌐 SUBMIT: https://www.uspto.gov/patents/apply")

if __name__ == "__main__":
    main()
