import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 環境変数を読み込み
load_dotenv()

class FAQManager:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.faqs = []  # FAQデータを保持（例: [{"q": "質問", "a": "回答"}]）

        # プロンプトテンプレートを定義
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "以下のFAQを参考に、質問に適切な回答を日本語で出力してください。"),
            ("human", "FAQ候補:\n{faq_block}\n\nユーザー質問: {question}")
        ])

        # プロンプト → LLM → 出力を文字列として受け取るチェーンを作成
        self.chain = self.prompt | self.llm | StrOutputParser()

    def add(self, q: str, a: str):
        """FAQアイテムを追加するメソッド"""
        self.faqs.append({"q": q, "a": a})

    def _search(self, question: str) -> list:
        """FAQを検索する簡易処理（キーワードマッチング）"""
        import re
        results = []
        # ユーザー質問を単語に分割
        question_words = set(re.findall(r'[ア-ンa-zA-Z0-9]+', question.lower()))

        for item in self.faqs:
            # FAQの質問と回答をまとめて検索対象にする
            content = (item["q"] + " " + item["a"]).lower()
            faq_words = set(re.findall(r'[ア-ンa-zA-Z0-9]+', content))

            # ユーザー質問とFAQの単語に共通部分があればヒットとみなす
            if question_words & faq_words:
                results.append(item)

        return results[:3]  # 最大3件まで返す

    def answer(self, question: str) -> str:
        """ユーザーの質問に対して回答を生成する"""
        hits = self._search(question)

        if not hits:
            return "該当するFAQが見つかりませんでした。"

        # ヒットしたFAQを文字列にまとめてプロンプトに埋め込む
        faq_block = "\n".join([f"Q: {item['q']}\nA: {item['a']}" for item in hits])

        # LLMに問い合わせて回答を生成
        return self.chain.invoke({
            "faq_block": faq_block,
            "question": question
        })


llm = ChatOpenAI(model="gpt-5-nano", api_key=os.getenv('OPENAI_API_KEY'))
faq = FAQManager(llm)

# FAQを登録
faq.add("インストール手順", "セットアップウィザードを起動し、画面の指示に従ってください。")
faq.add("アンインストール方法", "コントロールパネルからアプリを選択し、アンインストールを実行します。")

# ユーザーからの質問
question = "インストール方法が知りたい"
print(faq.answer(question))
