#!/usr/bin/env python3
"""
モデル設定を正しく修正：
- 2-1-2-* ファイルは gpt-4.1-nano（temperatureデモ用）
- それ以外は gpt-5-nano + temperature=1.0
"""
from pathlib import Path

# 2-1-2-* 以外のファイルを処理
changed = 0
for file in Path('.').glob('*-prompt.txt'):
    if not file.name.startswith('2-1-2-'):
        content = file.read_text()

        # モデルを gpt-5-nano に変更
        if 'model: gpt-4.1-nano' in content:
            content = content.replace('model: gpt-4.1-nano', 'model: gpt-5-nano')

        # temperature を 1.0 に変更
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if line.strip().startswith('temperature:'):
                new_lines.append('temperature: 1.0')
            else:
                new_lines.append(line)

        new_content = '\n'.join(new_lines)
        if new_content != file.read_text():
            file.write_text(new_content)
            changed += 1
            print(f'✅ {file.name}')

print(f'\n📊 {changed} ファイルを修正しました')