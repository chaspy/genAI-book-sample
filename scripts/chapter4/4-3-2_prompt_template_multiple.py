from langchain_core.prompts import PromptTemplate

template = """
あなたは翻訳アシスタントです。
以下の文章を {source_lang} から {target_lang} に翻訳してください。

文章: {source_text}
"""

prompt = PromptTemplate(
    input_variables=["source_lang", "target_lang", "source_text"],
    template=template
)

print(prompt.format(
    source_lang="日本語",
    target_lang="英語",
    source_text="お会いできてうれしいです。"
))
