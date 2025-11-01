import time
from functools import wraps
from dotenv import load_dotenv
import os
from openai import OpenAI, APIError, RateLimitError, AuthenticationError, BadRequestError

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def retry_on_error(max_retries=3, initial_delay=1.0, backoff_factor=2.0):
    """API呼び出しを再試行するデコレーター"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (APIError, RateLimitError) as e:
                    print(f"エラー: {e} | {attempt+1}回目の試行に失敗。{delay}秒後に再試行...")
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay)
                    delay *= backoff_factor
                except (AuthenticationError, BadRequestError) as e:
                    # 認証エラーやリクエストエラーは再試行しない
                    print(f"再試行不可なエラー: {e}")
                    raise
        return wrapper
    return decorator

@retry_on_error()
def call_openai(prompt):
    return client.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content

if __name__ == "__main__":
    print(call_openai("こんにちは、あなたについて一文で教えてください。"))
