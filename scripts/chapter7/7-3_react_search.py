"""LangChain の ReAct パターンで Web 検索→要約を行うサンプル。"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

# outputs/ ディレクトリの自動作成
Path("scripts/chapter7/outputs").mkdir(parents=True, exist_ok=True)

MAX_ITERATIONS = 5

OFFLINE_SEARCH_DATA = {
    "answer": (
        "2024 年の生成 AI 業界では導入率が 33% から 71% へ拡大し、顧客エンゲージメントやコスト管理、"
        "製品開発での活用が急増しています。ROI を得た企業はカスタム アプリケーション投資を加速しました。"
    ),
    "results": [
        {
            "url": "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai",
            "title": "The State of AI: Global survey",
            "content": "Use of generative AI increased from 33% in 2023 to 71% in 2024. Use of AI by business function ...",
        },
        {
            "url": "https://blogs.microsoft.com/blog/2024/11/12/idcs-2024-ai-opportunity-study-top-five-ai-trends-to-watch/",
            "title": "IDC's 2024 AI opportunity study",
            "content": "Generative AI drives customer engagement, topline growth, and cost management; custom deployments are rising...",
        },
        {
            "url": "https://menlovc.com/2024-the-state-of-generative-ai-in-the-enterprise/",
            "title": "2024: The State of Generative AI in the Enterprise",
            "content": "Generative AI became mission critical in 2024 as enterprise spending surged and bespoke solutions emerged...",
        },
    ],
}


def require_env(var_name: str) -> str:
    """環境変数を取得し、存在しなければエラー終了する"""
    value = os.getenv(var_name)
    if not value:
        sys.stderr.write(f"環境変数 {var_name} が設定されていません\n")
        sys.exit(1)
    return value


@tool("offline_search")
def offline_search(query: str) -> dict:
    """サンプルデータを返すオフライン検索ツール"""
    return {
        "query": query,
        "follow_up_questions": None,
        "answer": OFFLINE_SEARCH_DATA["answer"],
        "images": [],
        "results": OFFLINE_SEARCH_DATA["results"],
    }

def build_agent(model: str = "gpt-4o-mini", stop_sequence: bool = True) -> AgentExecutor:
    """ReAct エージェントを構築する"""
    load_dotenv()
    openai_api_key = require_env("OPENAI_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")

    print(f"\n=== 検証設定 ===")
    print(f"モデル: {model}")
    print(f"stop_sequence: {stop_sequence}")
    print("=" * 60 + "\n")

    llm = ChatOpenAI(
        model=model,
        temperature=0.3,  # 調査・制御系のため低めに設定
        api_key=openai_api_key,
    )

    if tavily_api_key:
        search_tool = TavilySearch(
            max_results=3,
            include_answer=True,
        )
    else:
        search_tool = offline_search

    prompt = PromptTemplate(
        input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
        template="""
あなたは調査と要約を専門とするアシスタントです。以下の質問に対し、必ずツールを使って最新情報を取得してから回答してください。

重要なルール:
- 必ず最初にツールで情報を検索してください
- 検索せずに答えることは禁止です
- 回答は検索結果に基づいて構築してください

利用可能なツール一覧:
{tool_names}

ツール詳細:
{tools}

利用方法:
```
Thought: 次に取るべきアクションを説明
Action: 使用するツール名
Action Input: ツールへの入力内容
```
ツールからの応答は Observation として返されます。

質問: {input}

思考過程:
{agent_scratchpad}

最終回答は必ず「Final Answer: 」で始め、各ポイントの末尾に出典URLを括弧付きで明記してください。
""",
    )

    agent = create_react_agent(
        llm=llm,
        tools=[search_tool],
        prompt=prompt,
        stop_sequence=stop_sequence,
    )

    return AgentExecutor(
        agent=agent,
        tools=[search_tool],
        max_iterations=MAX_ITERATIONS,
        verbose=True,
        handle_parsing_errors=True,
    )

def main(query: Optional[str] = None, model: str = "gpt-4o-mini", stop_sequence: bool = True) -> None:
    agent = build_agent(model=model, stop_sequence=stop_sequence)
    question = query or "2025年の生成 AI 業界の主要な動向を3つ教えてください"

    print("=== ReAct Agent による検索・要約 ===\n")
    print(f"質問: {question}\n")
    print("=" * 60)

    result = agent.invoke({"input": question})

    print("\n" + "=" * 60)
    print("最終回答:\n")
    print(result["output"])

    # 標準化されたサマリー出力
    # steps: 実行したイテレーション数
    steps = len(result.get("intermediate_steps", []))

    # tool_calls: ツール呼び出しの回数
    tool_calls = sum(1 for step in result.get("intermediate_steps", [])
                     if len(step) >= 2 and step[0] is not None)

    # sources: 取得したソース数（検索結果のURLを数える）
    sources = 0
    for step in result.get("intermediate_steps", []):
        if len(step) >= 2 and step[1] is not None:
            # ToolMessage の内容を解析
            import json
            try:
                if isinstance(step[1], dict):
                    results = step[1].get("results", [])
                    sources += len(results)
                elif isinstance(step[1], str):
                    data = json.loads(step[1])
                    sources += len(data.get("results", []))
            except:
                pass

    # satisfied: Final Answer が生成されたかどうか
    satisfied = "Final Answer:" in result.get("output", "")

    print(f"\n[Summary] steps={steps} tool_calls={tool_calls} sources={sources} satisfied={satisfied}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ReAct Agent による検索・要約")
    parser.add_argument("query", nargs="?", help="質問（省略時はデフォルト質問を使用）")
    parser.add_argument("--model", default="gpt-4o-mini", help="使用するLLMモデル（デフォルト: gpt-4o-mini）")
    parser.add_argument(
        "--stop-sequence",
        dest="stop_sequence",
        action="store_true",
        default=True,
        help="stop_sequence を有効化（デフォルト: True）",
    )
    parser.add_argument(
        "--no-stop-sequence",
        dest="stop_sequence",
        action="store_false",
        help="stop_sequence を無効化",
    )
    args = parser.parse_args()
    main(query=args.query, model=args.model, stop_sequence=args.stop_sequence)
