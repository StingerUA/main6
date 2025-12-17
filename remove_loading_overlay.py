#!/usr/bin/env python3
import re
from pathlib import Path

# Список файлов для обработки
files_to_process = [
    'gokturk-1/index.html',
    'gokturk-2/index.html',
    'mars/index.html',
    'iss/index.html',
    'sputnik/index.html',
    'zhurong/index.html',
    'hubble/index.html',
    'jameswebb/index.html',
    'voyager2/index.html',
    'opportunity/index.html',
]

repo_root = Path('/workspaces/website5')

def remove_loading_overlay_html(content):
    """Удалить HTML блок #loading-overlay"""
    # Ищем комментарий и весь блок div с id="loading-overlay"
    pattern = r'<!-- FUTURISTIC ALBASPACE LOADING OVERLAY -->\s*<div id="loading-overlay">.*?</div>\s*'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    return content

def remove_loading_overlay_css(content):
    """Удалить CSS стили для #loading-overlay"""
    # Удаляем CSS блок для #loading-overlay и его стили
    pattern = r'/\*\s*===+\s*FUTURISTIC ALBASPACE PRELOADER\s*===+\s*\*/\s*#loading-overlay\s*\{[^}]*\}(? :\s*#loading-overlay: :[^}]*\{[^}]*\})*(?:\s*\. loader-card\s*\{[^}]*\}(? :\s*\.loader-card::[^}]*\{[^}]*\})*)?(?:\s*\.[a-zA-Z-]+\s*\{[^}]*\})*'
    content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Альтернативный подход: удаляем от комментария до последней closing скобки анимации progressGlow
    pattern2 = r'/\*\s*===+\s*FUTURISTIC ALBASPACE PRELOADER\s*===+\s*\*/\s*.*?@keyframes progressGlow\s*\{[^}]*\}\s*'
    content = re.sub(pattern2, '', content, flags=re.DOTALL | re.IGNORECASE)
    
    return content

def remove_loading_overlay_script(content):
    """Удалить JavaScript для #loading-overlay"""
    # Ищем комментарий и весь script блок
    pattern = r'<!-- (? :ЛОГИКА ДЛЯ ПРЕЛОАДЕРА|ЛОГИКА ПРЕЛОАДЕРА 3D-МОДЕЛИ) -->\s*<script>.*?window\.addEventListener\("DOMContentLoaded".*?(? : setTimeout\(hideOverlay, 20000\);|\};\s*\};)\s*</script>'
    content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
    return content

def process_file(filepath):
    """Обработать один файл"""
    try:
        content = filepath.read_text(encoding='utf-8')
        original_content = content
        
        # Удаляем HTML
        content = remove_loading_overlay_html(content)
        
        # Удаляем CSS
        content = remove_loading_overlay_css(content)
        
        # Удаляем JavaScript
        content = remove_loading_overlay_script(content)
        
        if content != original_content:
            filepath.write_text(content, encoding='utf-8')
            return True, "✓ Updated"
        else:
            return False, "⊘ No changes"
    except Exception as e:
        return False, f"✗ Error: {str(e)}"

# Обработка файлов
print("🔍 Removing #loading-overlay from HTML files.. .\n")
changed_count = 0

for file_path in files_to_process:
    full_path = repo_root / file_path
    if not full_path.exists():
        print(f"⊘ {file_path}: File not found")
        continue
    
    success, message = process_file(full_path)
    print(f"{'✓' if success else '⊘'} {file_path}: {message}")
    if success:
        changed_count += 1

print(f"\n✅ Total processed: {changed_count}/{len(files_to_process)} files updated")
print("⚠️  NOTE: #preloader (global page loader) was preserved!")