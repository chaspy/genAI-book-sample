import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2025-08 現在の主要モデル価格（USD, per 1M tokens）
MODEL_PRICES = {
    "gpt-4o-mini": {"in": 0.15, "in_cached": 0.075, "out": 0.6},
    "gpt-5-nano": {"in": 0.05, "in_cached": 0.005, "out": 0.4},
}

DEFAULT_MODEL = "gpt-5-nano"  # 既定モデル（必要に応じて変更可）

class SimpleCostMonitor:
    def __init__(self, daily_budget=5.0):
        self.daily_budget = daily_budget
        self.today_cost = 0.0
        self.request_count = 0

    def calculate_cost(
        self,
        prompt_tokens: int,
        completion_tokens: int,
        model: str = DEFAULT_MODEL,
        cached_input_tokens: int = 0
    ) -> float:
        """
        トークン数からコスト(USD)を計算。
        - prompt_tokens: 通常入力トークン
        - completion_tokens: 出力トークン
        - cached_input_tokens: キャッシュ入力（RAGキャッシュ/Batch等）
        - model: MODEL_PRICES のキー
        """
        if model not in MODEL_PRICES:
            raise ValueError(f"未対応モデルです: {model}")

        p = MODEL_PRICES[model]
        cost_input = (prompt_tokens * p["in"]) / 1_000_000
        cost_input_cached = (cached_input_tokens * p["in_cached"]) / 1_000_000
        cost_output = (completion_tokens * p["out"]) / 1_000_000
        return cost_input + cost_input_cached + cost_output

    def track_usage(
        self,
        prompt_tokens: int,
        completion_tokens: int,
        model: str = DEFAULT_MODEL,
        cached_input_tokens: int = 0
    ) -> float:
        """使用量を追跡してアラートチェック"""
        cost = self.calculate_cost(prompt_tokens, completion_tokens, model, cached_input_tokens)
        self.today_cost += cost
        self.request_count += 1

        # アラートチェック
        if self.today_cost > self.daily_budget:
            print(f"予算超過: ${self.today_cost:.4f} (予算: ${self.daily_budget})")
        elif self.today_cost > self.daily_budget * 0.8:
            print(f"予算80%到達: ${self.today_cost:.4f}")

        print(f"今回: ${cost:.4f} | 累計: ${self.today_cost:.4f} ({self.request_count}回)")
        return cost

# 使用例
monitor = SimpleCostMonitor(daily_budget=1.0)  # 1日1ドル予算

def cost_aware_chat(prompt: str, model: str = DEFAULT_MODEL):
    """コスト監視付きチャット"""
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=1000
        )

        usage = resp.usage
        # Chat Completions の usage は cached_input_tokens を返さない想定なので 0 のまま
        monitor.track_usage(
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            model=model,
            cached_input_tokens=0
        )
        return resp.choices[0].message.content

    except Exception as e:
        print(f"エラー: {e}")
        return None

# デモ実行
if __name__ == "__main__":
    if os.getenv("OPENAI_API_KEYa"):
        result = cost_aware_chat("こんにちは", model=DEFAULT_MODEL)
        print(f"回答: {result}")
    else:
        # デモ計算（入力50 / 出力100トークン, gpt-5-nano）
        demo = monitor.calculate_cost(50, 100, model="gpt-5-nano")
        print(f"デモ: 50(in)+100(out) のコスト = ${demo:.6f}")
