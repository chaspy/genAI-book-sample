#!/usr/bin/env python3
"""
2-1-1: トークン数の最小例
書籍掲載のサンプル通りに、日本語と英語のトークン数を比較します。
"""

# pip install tiktoken
import tiktoken

def main():
    # GPT-4/3.5 系モデルで利用される cl100k_base エンコーディング
    encoding = tiktoken.get_encoding("cl100k_base")

    japanese_text = "デバッグする"
    english_text = "debug code"

    print(f"日本語: {len(encoding.encode(japanese_text))} トークン")
    print(f"英語: {len(encoding.encode(english_text))} トークン")

if __name__ == "__main__":
    main()
