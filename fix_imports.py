import os
import re

def fix_imports_in_file(file_path):
    """Fix relative imports in a file by replacing them with absolute imports"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace relative imports with absolute imports
    # Replace from ...module with from module
    content = re.sub(r'from \.\.\.([a-zA-Z_][a-zA-Z0-9_.]*)', r'from \1', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed imports in {file_path}")

# Fix imports in all API files
api_files = [
    'app/api/v1/slack.py',
    'app/api/v1/atlassian.py',
    'app/api/v1/notion.py',
    'app/api/v1/confluence.py',
    'app/api/v1/unified.py'
]

for file_path in api_files:
    if os.path.exists(file_path):
        fix_imports_in_file(file_path)
    else:
        print(f"File not found: {file_path}")

print("Import fixes completed!")
