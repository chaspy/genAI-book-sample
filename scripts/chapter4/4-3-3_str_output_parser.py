import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# プロンプト
prompt = ChatPromptTemplate.from_template(
    "次の文章を100文字以内で要約してください:\n{text}"
)

# モデル
model = ChatOpenAI(
    model="gpt-5-nano",
    api_key=os.getenv('OPENAI_API_KEY')
)

# 出力パーサー
parser = StrOutputParser()

# Chain: プロンプト → モデル → パーサー
chain = prompt | model | parser

target_text = """
LangChainは、大規模言語モデル（LLM）を活用したアプリケーション開発を支援するフレームワークです。
プロンプト設計や会話履歴の管理、外部データ検索、APIとの連携などをモジュール化して提供し、
必要な機能を組み合わせることで柔軟にアプリを構築できます。
チャットボットやRAGといった実用システム開発を効率化します。
"""

# 実行
result = chain.invoke({"text": target_text})
print(result)
