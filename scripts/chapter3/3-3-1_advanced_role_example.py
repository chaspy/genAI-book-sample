"""
OpenAI API の役割（role）システムを活用したサンプルコード
"""

from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_system_role(system_content, user_content):
    """システムロールを使用してAIの振る舞いを設定"""
    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

def main():
    """メイン実行関数"""
    print("=== システムロールの比較例 ===")

    # 技術専門家として設定
    tech_response = chat_with_system_role(
        "あなたは技術的な質問に正確に答える専門家です。",
        "LLMとは何ですか？"
    )
    if tech_response:
        print("技術専門家として:")
        print(tech_response)

    print("\n" + "="*50 + "\n")

    # 初心者向けアシスタントとして設定
    beginner_response = chat_with_system_role(
        "あなたは初心者にも分かりやすく説明する親切なアシスタントです。",
        "LLMとは何ですか？"
    )
    if beginner_response:
        print("初心者向けアシスタントとして:")
        print(beginner_response)

if __name__ == "__main__":
    # APIキーの存在確認
    if not os.getenv("OPENAI_API_KEY"):
        print("エラー: OPENAI_API_KEY が設定されていません。")
        print(".env ファイルに OPENAI_API_KEY=your_api_key_here を記載してください。")
    else:
        main()
