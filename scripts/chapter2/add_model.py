#!/usr/bin/env python3
"""
model設定がないプロンプトファイルにgpt-5-nanoを追加
"""
from pathlib import Path

PROMPTS_DIR = Path("prompts")
PROMPTS_DIR.mkdir(exist_ok=True)

def add_model_to_prompt_file(file_path):
    """プロンプトファイルにモデル設定を追加"""
    content = file_path.read_text()

    if not content.startswith('---'):
        return False

    lines = content.split('\n')

    # metadataセクションを見つける
    meta_end = lines[1:].index('---') + 1
    metadata = lines[1:meta_end]

    # model行がすでにあるかチェック
    if any('model:' in line for line in metadata):
        return False

    # temperature行を見つけて、その後にmodel行を追加
    new_lines = [lines[0]]  # 最初の---

    for line in metadata:
        new_lines.append(line)
        if 'temperature:' in line:
            new_lines.append('model: gpt-5-nano')

    # 残りの行を追加
    new_lines.extend(lines[meta_end:])

    # ファイルに書き戻す
    file_path.write_text('\n'.join(new_lines))
    return True

# すべてのプロンプトファイルを処理
modified_files = []
for file in PROMPTS_DIR.glob('*-prompt.txt'):
    if add_model_to_prompt_file(file):
        modified_files.append(file.name)
        print(f"✅ Updated: {file.name}")

print(f"\n📊 総計: {len(modified_files)} ファイルを更新しました")
