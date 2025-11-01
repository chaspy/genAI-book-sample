#!/usr/bin/env python3
"""
2-1-1: トークン数の計測
tiktoken を使って日本語と英語のトークン数を比較します。
"""

# pip install tiktoken
import tiktoken
import sys
from pathlib import Path

def count_tokens(text, encoding_name="cl100k_base"):
    """指定されたテキストのトークン数を計算"""
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)
    return len(tokens)

def visualize_tokens(text, encoding_name="cl100k_base"):
    """トークン分割を可視化"""
    encoding = tiktoken.get_encoding(encoding_name)
    
    # テキストをトークンIDにエンコード
    token_ids = encoding.encode(text)
    
    # 各トークンIDを文字列にデコード
    tokens = []
    for token_id in token_ids:
        # トークンIDから文字列に変換
        token_str = encoding.decode([token_id])
        tokens.append(token_str)
    
    return tokens, token_ids

def main():
    # エンコーディングを取得（GPT-4/3.5用）
    encoding = tiktoken.get_encoding("cl100k_base")
    
    # 出力を収集
    output_lines = []
    
    def print_and_collect(text=""):
        """標準出力に表示し、同時に出力リストに追加"""
        print(text)
        output_lines.append(text)
    
    print_and_collect("=" * 50)
    print_and_collect("トークン数の計測とトークン分割の可視化")
    print_and_collect("=" * 50)
    
    # 基本的な例
    japanese_text = "こんにちは世界"
    english_text = "Hello World"
    
    print_and_collect(f"\n【日本語】 '{japanese_text}'")
    jp_tokens, jp_ids = visualize_tokens(japanese_text)
    print_and_collect(f"トークン数: {len(jp_tokens)} トークン")
    print_and_collect(f"トークン分割: {' | '.join(f'[{token}]' for token in jp_tokens)}")
    print_and_collect(f"トークンID: {jp_ids}")
    
    print_and_collect(f"\n【英語】 '{english_text}'")
    en_tokens, en_ids = visualize_tokens(english_text)
    print_and_collect(f"トークン数: {len(en_tokens)} トークン")
    print_and_collect(f"トークン分割: {' | '.join(f'[{token}]' for token in en_tokens)}")
    print_and_collect(f"トークンID: {en_ids}")
    
    # より詳細な比較
    print_and_collect("\n" + "=" * 50)
    print_and_collect("トークンの詳細比較")
    print_and_collect("=" * 50)
    
    examples = [
        ("データベース", "Database"),
        ("こんにちは世界", "Hello World"),
        ("人工知能", "Artificial Intelligence"),
        ("データベースのインデックス", "Database index"),
    ]
    
    for jp_text, en_text in examples:
        jp_tokens_list, _ = visualize_tokens(jp_text)
        en_tokens_list, _ = visualize_tokens(en_text)
        jp_tokens = len(jp_tokens_list)
        en_tokens = len(en_tokens_list)
        ratio = jp_tokens / en_tokens if en_tokens > 0 else 0
        
        print_and_collect(f"\n日本語: {jp_text}")
        print_and_collect(f"  トークン分割: {' | '.join(f'[{t}]' for t in jp_tokens_list)}")
        print_and_collect(f"  → {jp_tokens} トークン")
        print_and_collect(f"英語: {en_text}")
        print_and_collect(f"  トークン分割: {' | '.join(f'[{t}]' for t in en_tokens_list)}")
        print_and_collect(f"  → {en_tokens} トークン")
        print_and_collect(f"比率: {ratio:.2f}倍")
    
    # コスト計算の例
    print_and_collect("\n" + "=" * 50)
    print_and_collect("API利用料金の見積もり例")
    print_and_collect("=" * 50)
    
    # 想定: 1日100回の問い合わせ、各1000トークン
    daily_queries = 100
    tokens_per_query = 1000
    days_per_month = 30
    
    # GPT-4の料金（例: $0.03/1000トークン）
    price_per_1k_tokens = 0.03
    
    monthly_tokens = daily_queries * tokens_per_query * days_per_month
    monthly_cost = (monthly_tokens / 1000) * price_per_1k_tokens
    
    print_and_collect(f"\n前提条件:")
    print_and_collect(f"  - 1日の問い合わせ数: {daily_queries}回")
    print_and_collect(f"  - 1回あたりのトークン数: {tokens_per_query}トークン")
    print_and_collect(f"  - 月間日数: {days_per_month}日")
    print_and_collect(f"  - 料金: ${price_per_1k_tokens}/1000トークン")
    
    print_and_collect(f"\n計算結果:")
    print_and_collect(f"  - 月間トークン数: {monthly_tokens:,}トークン")
    print_and_collect(f"  - 月額費用: ${monthly_cost:.2f} (約{monthly_cost * 150:.0f}円)")
    
    # 長文のトークン数計測
    print_and_collect("\n" + "=" * 50)
    print_and_collect("長文のトークン分割の可視化")
    print_and_collect("=" * 50)
    
    long_text = """データベースのインデックスとは、データベースの検索性能を向上させる仕組みです。"""
    
    tokens_list, token_ids = visualize_tokens(long_text)
    tokens = len(tokens_list)
    
    print_and_collect(f"\nサンプル文章（{len(long_text)}文字）:")
    print_and_collect(f"「{long_text}」")
    print_and_collect(f"\nトークン分割:")
    # トークンを見やすく表示（10トークンごとに改行）
    for i in range(0, len(tokens_list), 10):
        chunk = tokens_list[i:i+10]
        print_and_collect(f"  {' | '.join(f'[{t}]' for t in chunk)}")
    
    print_and_collect(f"\nトークン数: {tokens}トークン")
    print_and_collect(f"文字数/トークン数比: {len(long_text) / tokens:.2f}")
    
    # 特殊な例の可視化
    print_and_collect("\n" + "=" * 50)
    print_and_collect("特殊な例のトークン分割")
    print_and_collect("=" * 50)
    
    special_examples = [
        "AI",
        "人工知能",
        "ChatGPT",
        "😊",
        "123",
        "こんにちは！",
        "Hello, World!",
        "B-tree",
        "データベース",
        "インデックス",
    ]
    
    for text in special_examples:
        tokens_list, _ = visualize_tokens(text)
        print_and_collect(f"\n'{text}' → {' | '.join(f'[{t}]' for t in tokens_list)} ({len(tokens_list)}トークン)")

    # ファイルに保存
    output_file = Path("2-1-1-out.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"\n✅ 出力を保存しました: {output_file}")

if __name__ == "__main__":
    main()