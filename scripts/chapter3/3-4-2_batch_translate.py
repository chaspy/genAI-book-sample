import asyncio
import time
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class TranslationManager:
    def __init__(self, api_key: str, max_concurrent: int = 5):
        self.client = OpenAI(api_key=api_key)
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.request_times = []

    async def translate_single(self, text: str, retries: int = 3) -> str:
        """レートリミット対策付き単文翻訳"""
        async with self.semaphore:
            for attempt in range(retries):
                try:
                    # レートリミット調整
                    await self._rate_limit_check()

                    response = self.client.chat.completions.create(
                        model="gpt-5-nano",
                        messages=[
                            {"role": "user", "content": f"Translate to Japanese: {text}"}
                        ],
                        temperature=0.3
                    )

                    self.request_times.append(time.time())
                    return response.choices[0].message.content

                except Exception as e:
                    if attempt == retries - 1:
                        return f"翻訳失敗: {text} (エラー: {str(e)})"
                    await asyncio.sleep(2 ** attempt)  # 指数バックオフ

    async def _rate_limit_check(self):
        """1分間のリクエスト数を制御"""
        current_time = time.time()
        self.request_times = [t for t in self.request_times if current_time - t < 60]

        if len(self.request_times) >= 50:  # 1分間50リクエスト制限
            sleep_time = 60 - (current_time - self.request_times[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)

    async def batch_translate(self, texts: List[str]) -> List[str]:
        """バッチ翻訳の実行"""
        tasks = [self.translate_single(text) for text in texts]
        return await asyncio.gather(*tasks)

# 使用例
async def main():
    texts = [
        "Good morning.",
        "This is a sample translation.",
        "Please review the report."
    ]

    manager = TranslationManager(os.getenv("OPENAI_API_KEY"))
    results = await manager.batch_translate(texts)

    for original, translated in zip(texts, results):
        print(f"原文: {original}")
        print(f"翻訳: {translated}\n")

asyncio.run(main())
