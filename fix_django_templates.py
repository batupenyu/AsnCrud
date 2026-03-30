# -*- coding: utf-8 -*-
"""
Fix Django template tags that are broken across multiple lines.
Run this script if templates get broken again.
"""
import re
import os

def fix_template_tags(content):
    """Join broken {% %} and {{ }} tags across multiple lines."""
    lines = content.split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for unclosed {% tag
        if '{%' in line and '%}' not in line:
            while i + 1 < len(lines) and '%}' not in line:
                i += 1
                line += ' ' + lines[i].strip()
            result.append(line)
        # Check for unclosed {{ variable  
        elif '{{' in line and '}}' not in line:
            while i + 1 < len(lines) and '}}' not in line:
                i += 1
                line += ' ' + lines[i].strip()
            result.append(line)
        else:
            result.append(line)
        i += 1
    
    return '\n'.join(result)

def clean_spaces(content):
    """Clean up extra spaces in template tags."""
    content = re.sub(r'\{%\s+', r'{% ', content)
    content = re.sub(r'\s+%\}', r' %}', content)
    content = re.sub(r'\{\{\s+', r'{{ ', content)
    content = re.sub(r'\s+\}\}', r' }}', content)
    return content

def fix_file(filepath):
    """Fix a single template file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = fix_template_tags(content)
    content = clean_spaces(content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'Fixed: {filepath}')

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(base_dir, 'asn_app', 'templates', 'asn_app')
    
    fix_file(os.path.join(templates_dir, 'spt_pdf_template.html'))
    fix_file(os.path.join(templates_dir, 'spt_pdf_template_large.html'))
    
    print('\nDone! Templates fixed.')
