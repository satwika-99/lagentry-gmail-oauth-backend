#!/usr/bin/env python3
"""
Script to fix all import statements in the app directory
"""

import os
import re

def fix_imports_in_file(file_path):
    """Fix import statements in a single file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix imports
    original_content = content
    
    # Fix core imports
    content = re.sub(r'from core\.', 'from app.core.', content)
    content = re.sub(r'import core\.', 'import app.core.', content)
    
    # Fix api imports
    content = re.sub(r'from api\.', 'from app.api.', content)
    content = re.sub(r'import api\.', 'import app.api.', content)
    
    # Fix schemas imports
    content = re.sub(r'from schemas\.', 'from app.schemas.', content)
    content = re.sub(r'import schemas\.', 'import app.schemas.', content)
    
    # Fix services imports
    content = re.sub(r'from services\.', 'from app.services.', content)
    content = re.sub(r'import services\.', 'import app.services.', content)
    
    # Fix providers imports
    content = re.sub(r'from providers\.', 'from app.providers.', content)
    content = re.sub(r'import providers\.', 'import app.providers.', content)
    
    # Fix connectors imports
    content = re.sub(r'from connectors\.', 'from app.connectors.', content)
    content = re.sub(r'import connectors\.', 'import app.connectors.', content)
    
    # Fix models imports
    content = re.sub(r'from models\.', 'from app.models.', content)
    content = re.sub(r'import models\.', 'import app.models.', content)
    
    # Fix storage imports
    content = re.sub(r'from storage\.', 'from app.storage.', content)
    content = re.sub(r'import storage\.', 'import app.storage.', content)
    
    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed imports in {file_path}")
        return True
    return False

def fix_imports_in_directory(directory):
    """Fix imports in all Python files in a directory recursively"""
    fixed_count = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if fix_imports_in_file(file_path):
                    fixed_count += 1
    
    return fixed_count

if __name__ == "__main__":
    app_dir = "app"
    if os.path.exists(app_dir):
        print(f"Fixing imports in {app_dir} directory...")
        fixed = fix_imports_in_directory(app_dir)
        print(f"Fixed imports in {fixed} files")
    else:
        print(f"Directory {app_dir} not found")
