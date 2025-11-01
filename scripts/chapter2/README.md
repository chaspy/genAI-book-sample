# Chapter 2 サンプルコード

第2章「Prompt Engineering」のサンプルコード集です。

## 🎯 学習目標

- LLMの基本パラメータ（Temperature、トークン）の理解
- プロンプトパターン（Zero-Shot、Few-Shot、CoT）の実践
- 実務で使えるプロンプト設計スキルの習得

## 📁 新しいファイル構成

### 独立したスクリプト
- `2-1-1.py` - tiktoken によるトークン数計測（LLM API不要）

### LLM API呼び出し用
- `call-llm.py` - 共通のLLM API呼び出しスクリプト
- `*-prompt.txt` - 各例のプロンプトファイル
- `*-out.txt` - 実行結果（自動生成）

## 📋 必要な環境

- Python 3.10以上（推奨: 3.11.9）
- OpenAI API キー（[取得方法](https://platform.openai.com/api-keys)）

## 🚀 簡単な使い方

### セットアップ
```bash
# 必要なパッケージのインストール
pip install openai tiktoken

# .envrc ファイルを編集してAPIキーを設定
vi .envrc  # OPENAI_API_KEY の値を実際のキーに変更

# 環境変数を読み込む
source .envrc
```

### トークン数計測（2-1-1）
```bash
python 2-1-1.py
```

### LLM API呼び出し
```bash
# 基本的な実行
python call-llm.py 2-1-2

# Temperature を変えて実行
python call-llm.py 2-1-2 --temperature 1.5

# 複数回実行して比較
python call-llm.py 2-1-2 --repeat 5 --temperature 0.8

# システムプロンプトを指定
python call-llm.py 2-2-3 --system "あなたは専門家です"
```

### 動作確認
```bash
# すべての基本機能をテスト
./test.sh
```

### 全プロンプトの一括実行
```bash
# 全プロンプトファイルを順番に実行
python run-all.py

# または直接実行
./run-all.py
```

## 📚 プロンプトファイル一覧

| ファイルID | 説明 | 主なテーマ |
|-----------|-----|----------|
| 2-1-2 | Temperature パラメータのデモ | 出力の多様性制御 |
| 2-2-1 | 明確な指示の例 | プロンプトの明確性 |
| 2-2-2 | 肯定的な指示の例 | 否定形 vs 肯定形 |
| 2-2-3 | 技術文書レビュー | System Prompt活用 |
| 2-3-1 | 感情分析 | Few-Shot学習 |
| 2-3-2 | 価格の構造化 | エッジケース対応 |
| 2-4-1 | 数学問題 | Chain-of-Thought |
| 2-4-2 | 在庫管理問題 | ステップバイステップ |

## 📝 プロンプトファイルの形式

```
---
temperature: 0.7
system: システムプロンプト（オプション）
description: 説明
---
ここにプロンプト本文
```

## 💾 出力ファイルの形式

実行結果は `{ID}-out.txt` に自動保存されます：

```
---
model: gpt-3.5-turbo
temperature: 0.7
max_tokens: 500
executions: 1
has_system_prompt: no
---

LLMの応答がここに記録されます
```

## 🚀 以前のクイックスタート（レガシー）

最も簡単な方法（Make使用）:

```bash
# 1. 環境構築
make setup

# 2. API キー設定
cp .env.example .env
# .envファイルを編集してAPIキーを設定

# 3. デモ実行
make demo
```

## 📦 環境構築方法（再現性重視）

### 方法1: uv（推奨・高速）

```bash
# uvのインストール（初回のみ）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 環境構築
uv venv
uv pip sync pyproject.toml

# 環境有効化
source .venv/bin/activate
```

### 方法2: Docker（完全分離環境）

```bash
# イメージビルド
docker build -t genai-book-chapter2 .

# 実行
docker run --rm -it --env-file .env genai-book-chapter2 \
  python 2-1-2_temperature_demo.py --demo
```

### 方法4: 対話式セットアップ

```bash
# setupスクリプトを実行（環境を自動判定）
bash setup.sh
```

## 🔑 API キー設定

```bash
# .envファイルを作成
cp .env.example .env

# .envファイルを編集
vim .env  # または好きなエディタで
# OPENAI_API_KEY=sk-... # あなたのAPIキーに置き換え
```

## 📚 スクリプト一覧

| ファイル | 内容 | 対応セクション | 実行例 |
|---------|------|--------------|--------|
| `2-0_prompt_examples.py` | プロンプト実例集 | 全体 | `python 2-0_prompt_examples.py --list` |
| `2-1-1_tokenizer_demo.py` | トークン分割の可視化 | 2-1-1 | `python 2-1-1_tokenizer_demo.py` |
| `2-1-1_token_counter.py` | トークン数カウント | 2-1-1 | `python 2-1-1_token_counter.py -t "テキスト"` |
| `2-1-1_token_optimizer.py` | トークン最適化 | 2-1-1 | `python 2-1-1_token_optimizer.py` |
| `2-1-2_temperature_demo.py` | Temperature効果検証 | 2-1-2 | `python 2-1-2_temperature_demo.py --demo` |
| `2-1-3_message_role_demo.py` | メッセージロール比較 | 2-1-3 | `python 2-1-3_message_role_demo.py --system` |
| `2-4_chain_of_thought_demo.py` | CoT効果実証 | 2-4 | `python 2-4_chain_of_thought_demo.py --math` |
| `2-5-2_api_client_generator.py` | APIクライアント生成 | 2-5-2 | `python 2-5-2_api_client_generator.py` |
| `2-5-3_data_analysis_example.py` | データ分析例 | 2-5-3 | `python 2-5-3_data_analysis_example.py --sales` |
| `2-7-1_prompt_evaluator.py` | プロンプト評価システム（シミュレータ版） | 2-7-1 | `python 2-7-1_prompt_evaluator.py` |
| `2-7-2_working_evaluator.py` | プロンプト評価システム（OpenAI API版） | 2-7-2 | `python 2-7-2_working_evaluator.py` |

## 🔬 実行例

### Temperature効果の検証

```bash
# デフォルトのデモ（Temperature 0.2, 0.5, 0.7, 0.9で比較）
python 2-1-2_temperature_demo.py --demo

# カスタムプロンプトで実験
python 2-1-2_temperature_demo.py --prompt "明日の天気を詩的に表現してください"
```

### メッセージロールの効果

```bash
# システムロールの効果検証
python 2-1-3_message_role_demo.py --system

# 会話履歴の維持
python 2-1-3_message_role_demo.py --conversation

# API vs UI の違い説明
python 2-1-3_message_role_demo.py --explanation
```

### Chain-of-Thought

```bash
# 数学問題での効果
python 2-4_chain_of_thought_demo.py --math

# 推論過程の可視化
python 2-4_chain_of_thought_demo.py --reasoning
```

### プロンプト評価システム

```bash
# シミュレータ版（APIキー不要）
python 2-7-1_prompt_evaluator.py

# OpenAI API版（実際のLLMを使用）
python 2-7-2_working_evaluator.py

# 評価結果はJSONファイルに保存
cat evaluation_results.json
```

## 🧪 すべてのデモを実行

```bash
# Makefileを使用
make demo-all

# または個別に実行
python 2-1-2_temperature_demo.py --demo
python 2-1-3_message_role_demo.py --system
python 2-4_chain_of_thought_demo.py --math
```

## 📄 実行結果の参照

本文中の例は実際にスクリプトを実行した結果を使用しています：

```bash
# 本文引用用の出力を生成
make generate-outputs

# 生成された出力を確認
ls outputs/
```

生成される出力ファイル：
- `outputs/temperature_demo_output.txt` - Temperature効果の実例
- `outputs/message_role_output.txt` - メッセージロール効果
- `outputs/cot_math_output.txt` - Chain-of-Thought実証

これらの出力はGitリポジトリにコミットされており、本文から参照されています。

## 📁 ファイル構成

```
scripts/chapter2/
├── README.md                        # このファイル
├── pyproject.toml                   # uv用設定ファイル
├── .python-version                  # Pythonバージョン指定（3.11.9）
├── .env.example                     # 環境変数テンプレート
├── setup.sh                         # 対話式セットアップスクリプト
├── Makefile                         # よく使うコマンド集
├── Dockerfile                       # Docker環境定義
├── test_temperature.sh              # Temperature効果の実行テスト
├── 2-0_prompt_examples.py           # プロンプト実例集
├── 2-1-1_tokenizer_demo.py          # トークン分割デモ
├── 2-1-1_token_counter.py           # トークンカウンター
├── 2-1-1_token_optimizer.py         # トークン最適化
├── 2-1-2_temperature_demo.py        # Temperature効果デモ
├── 2-1-3_message_role_demo.py       # メッセージロールデモ
├── 2-4_chain_of_thought_demo.py     # CoTデモ
├── 2-5-2_api_client_generator.py    # APIクライアント生成
├── 2-5-3_data_analysis_example.py   # データ分析例
├── 2-7-1_prompt_evaluator.py        # プロンプト評価（シミュレータ）
└── 2-7-2_working_evaluator.py       # プロンプト評価（OpenAI API）
```

## 🐛 トラブルシューティング

### APIキーエラー

```
Error: No API key provided
```

**解決方法:**
1. `.env`ファイルが存在するか確認: `ls -la .env`
2. APIキーが正しく設定されているか確認: `grep OPENAI_API_KEY .env`
3. 環境変数として読み込まれているか確認: `echo $OPENAI_API_KEY`

### モジュールエラー

```
ModuleNotFoundError: No module named 'openai'
```

**解決方法:**
```bash
# パッケージを再インストール
uv sync
```

### バージョンエラー

```
Python 3.10+ required
```

**解決方法:**
```bash
# 現在のバージョン確認
python --version

# pyenvでPython 3.11.9をインストール
pyenv install 3.11.9
pyenv local 3.11.9

# または公式インストーラーを使用
# https://www.python.org/downloads/
```

### Docker実行エラー

```
docker: command not found
```

**解決方法:**
- Docker Desktopをインストール: https://docs.docker.com/get-docker/

## 🔄 環境の再現性について

このプロジェクトは複数の方法で環境を再現できるよう設計されています：

1. **バージョン固定**: `pyproject.toml`と`uv.lock`でパッケージバージョンを固定
2. **Pythonバージョン**: `.python-version`で3.11.9を指定
3. **Docker**: 完全に同一の実行環境を提供
4. **環境変数管理**: `.env.example`による設定テンプレート

チーム開発や異なるPC間での作業時も、同じ結果が得られることを保証します。

## 📖 参考資料

- [OpenAI API ドキュメント](https://platform.openai.com/docs)
- [tiktoken ドキュメント](https://github.com/openai/tiktoken)
- [uv ドキュメント](https://github.com/astral-sh/uv)
- 書籍第2章の該当セクション

## 💡 活用のポイント

1. **まずは動かしてみる**: `make demo`で基本動作を確認
2. **パラメータを変えて実験**: Temperature値を変更して効果を体感
3. **自分のプロンプトで試す**: カスタムプロンプトオプションを活用
4. **コストを意識**: トークンカウンターでAPI利用料を把握
5. **バージョン管理**: 効果的なプロンプトはGitで管理

---

これらのツールを活用して、実践的なプロンプトエンジニアリングスキルを身につけましょう！