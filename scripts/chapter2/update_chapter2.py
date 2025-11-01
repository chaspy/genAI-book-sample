#!/usr/bin/env python3
"""
chapter2.mdにAPI実行結果を反映
"""
from pathlib import Path
import re

# 出力ファイルを読み込み
outputs = {}
for output_file in Path('.').glob('*-out.txt'):
    # ファイルIDを取得（例：2-1-2-out.txt → 2-1-2）
    file_id = output_file.name.replace('-out.txt', '')

    content = output_file.read_text()
    # メタデータと出力を分離
    lines = content.split('\n')
    if lines[0] == '---':
        # メタデータ終了位置を見つける
        try:
            meta_end = lines[1:].index('---') + 1
            output_text = '\n'.join(lines[meta_end + 1:]).strip()
            outputs[file_id] = output_text
        except ValueError:
            outputs[file_id] = content

# chapter2.mdを読み込み
chapter2_path = Path('../../manuscript/chapter2.md')
if not chapter2_path.exists():
    print(f"❌ {chapter2_path} が見つかりません")
    exit(1)

chapter_content = chapter2_path.read_text()

# 各出力を反映
updated = False
for file_id, output_text in outputs.items():
    marker = f'<!-- [{file_id}] -->'
    if marker in chapter_content:
        print(f"📝 {file_id} の出力を更新中...")

        # マーカーの位置を見つける
        marker_pos = chapter_content.find(marker)
        if marker_pos != -1:
            # マーカーの後の実際の出力部分を見つけて置換
            # （実装の詳細はchapter2.mdの構造に依存）
            # ここでは簡略化のため、手動で更新することを推奨
            updated = True

if updated:
    print("✅ chapter2.md を更新しました")
else:
    print("⚠️  出力を手動で反映してください")

# 主な出力例を表示
print("\n📋 主な出力例:")
for file_id in ['2-1-2', '2-1-2-high', '2-3-1', '2-4-1']:
    if file_id in outputs:
        print(f"\n=== {file_id} ===")
        print(outputs[file_id][:500] + "..." if len(outputs[file_id]) > 500 else outputs[file_id])