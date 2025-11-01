import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# 環境変数を読み込み
load_dotenv()

# LLMモデルを初期化
llm = ChatOpenAI(
    model="gpt-5-nano",
    api_key=os.getenv('OPENAI_API_KEY')
)

# プロンプトテンプレートを作成
prompt = ChatPromptTemplate.from_messages([
    ("system", "あなたは親切なアシスタントです。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# チェーンを作成
chain = prompt | llm

# メッセージ履歴を初期化
message_history = ChatMessageHistory()

def get_session_history(session_id: str) -> ChatMessageHistory:
    return message_history

# RunnableWithMessageHistoryでメモリ機能を追加
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# 会話を実行
config = {"configurable": {"session_id": "abc123"}}

print(chain_with_history.invoke(
    {"input": "こんにちは！私は田中といいます。普段はエンジニアとして働いています。趣味はキャンプです。"},
    config=config
).content)

print(chain_with_history.invoke(
    {"input": "さっきの自己紹介を要約して。"},
    config=config
).content)
