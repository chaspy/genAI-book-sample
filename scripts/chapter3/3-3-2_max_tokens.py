from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

def adaptive_token_chat(prompt: str, output_type: str = "explanation"):
    # 用途別トークン数の目安
    token_guidelines = {
        "short_answer": 50,        # はい/いいえ、単語回答
        "summary": 150,            # 要約、概要
        "explanation": 300,        # 詳しい説明
        "article": 800,            # 記事、レポート
        "detailed_analysis": 1500, # 詳細分析、長文
    }

    # プロンプト長に応じて調整
    prompt_length = len(prompt.split())
    base_tokens = token_guidelines.get(output_type, 300)

    # 長いプロンプトの場合は出力を増加
    if prompt_length > 100:
        max_completion_tokens = min(int(base_tokens * 1.5), 1000)
    else:
        max_completion_tokens = base_tokens

    print(f"プロンプト長: {prompt_length}語 → トークン設定: {max_completion_tokens}")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=max_completion_tokens,
        temperature=0.7
    )

    return response.choices[0].message.content

# 使用例
if __name__ == "__main__":
    # 短い質問
    short_prompt = "LLMとは？"
    print(f"質問: {short_prompt}")
    answer = adaptive_token_chat(short_prompt, "short_answer")
    print(f"回答: {answer}\n")

    # 詳しい質問
    detailed_prompt = "機械学習における深層学習の役割と主要なアプリケーション領域について説明してください"
    print(f"質問: {detailed_prompt}")
    answer = adaptive_token_chat(detailed_prompt, "explanation")
    print(f"回答: {answer}")
