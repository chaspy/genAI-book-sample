#!/usr/bin/env python3
"""
2-1-1: 日英トークン分割の比較
書籍の解説をそのまま追体験できるよう、ステップごとに計算過程を表示するスクリプト。
"""

from __future__ import annotations

import tiktoken
from typing import List, Sequence, Tuple

Encoding = tiktoken.Encoding

def tokenize(text: str, encoding: Encoding) -> Tuple[List[str], List[int]]:
    token_ids = encoding.encode(text)
    readable_tokens: List[str] = []

    for token_id in token_ids:
        token_bytes = encoding.decode_single_token_bytes(token_id)
        try:
            token_str = token_bytes.decode("utf-8")
            if not token_str:
                raise UnicodeDecodeError("utf-8", token_bytes, 0, len(token_bytes), "empty string")
        except UnicodeDecodeError:
            token_str = "".join(f"\\x{b:02X}" for b in token_bytes)
        readable_tokens.append(token_str)

    return readable_tokens, token_ids

def format_tokens(tokens: Sequence[str]) -> str:
    return "|".join(f"[{token}]" for token in tokens)

def describe_pair(label: str, jp_text: str, en_text: str, encoding: Encoding) -> Tuple[int, int]:
    print(label)
    jap_tokens, _ = tokenize(jp_text, encoding)
    eng_tokens, _ = tokenize(en_text, encoding)
    print(f"日本語:「{jp_text}」→{format_tokens(jap_tokens)}({len(jap_tokens)}トークン)")
    print(f"英語:「{en_text}」→{format_tokens(eng_tokens)}({len(eng_tokens)}トークン)")
    return len(jap_tokens), len(eng_tokens)

def main() -> None:
    encoding = tiktoken.get_encoding("cl100k_base")

    # 例1: 単語レベルで日本語/英語の境界を確認
    describe_pair("最初の例で、トークンがどこで区切られるか見てみましょう。", "人工知能", "ArtificialIntelligence", encoding)

    print()
    # 例2: 完結した文章を比較
    jp_count, en_count = describe_pair("別の例で、文章全体のトークン分割を見てみます。", "デバッグする", "Debugcode", encoding)

    ratio = jp_count / en_count if en_count else 0
    print(
        f"\n同じ内容でも言語によってトークン数が変わり、日本語の方が高コストになる傾向があります。"
        f"この例では約{ratio:.2f}倍で、さらに差が大きくなるケースもあります。"
    )

    print()
    # 例3: 短い挨拶フレーズで倍率を確認
    greet_jp, greet_en = describe_pair("単純な挨拶では1.5倍程度になることもあります。", "やあ！", "Hello!", encoding)
    greet_ratio = greet_jp / greet_en if greet_en else 0
    print(f"  → 上記の挨拶は約{greet_ratio:.2f}倍です。")

    print(
        "\nちなみに、日本語は『1文字=1トークン』とは限りません。例えば『人工知能』は"
        " [人]|[工]|[知]|[能] と4トークンですが、『世界』は先頭の『世』だけで複数トークンに分割されます。"
    )
    # 例4: 1文字の内部構造をバイト列で観察
    world_tokens, _ = tokenize("世界", encoding)
    print(f"『世界』→{format_tokens(world_tokens)}({len(world_tokens)}トークン)")
    print(
        "  → 先頭2トークン (\\xE4\\xB8|\\x96) を結合すると1文字『世』となり、バイトレベルBPEにより1〜3トークンの幅が生じます。"
    )

if __name__ == "__main__":
    main()
