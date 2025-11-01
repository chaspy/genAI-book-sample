from langchain.prompts import PromptTemplate

# プロンプトのひな型を定義
template = "次の文章を英語に翻訳してください：\n{source_text}"

prompt = PromptTemplate(
    input_variables=["source_text"],
    template=template
)

print(prompt.format(source_text="今日はいい天気ですね。"))
