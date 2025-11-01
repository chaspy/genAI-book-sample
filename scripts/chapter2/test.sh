#!/bin/bash
# 動作確認スクリプト

echo "================================"
echo "Chapter 2 スクリプト動作確認"
echo "================================"

# 環境変数を読み込む
if [ -f .envrc ]; then
    echo "✅ .envrc を読み込みます..."
    source .envrc
else
    echo "❌ .envrc が見つかりません"
    exit 1
fi

# APIキーの確認
if [ "$OPENAI_API_KEY" = "your-api-key-here" ]; then
    echo "⚠️  APIキーが設定されていません"
    echo "   .envrc を編集して実際のAPIキーを設定してください"
    echo ""
fi

echo ""
echo "1. トークン数計測テスト (API不要)"
echo "--------------------------------"
python 2-1-1.py | head -20

echo ""
echo "2. LLM API呼び出しテスト"
echo "--------------------------------"
if [ "$OPENAI_API_KEY" != "your-api-key-here" ] && [ -n "$OPENAI_API_KEY" ]; then
    echo "Temperature デモを実行します..."
    python call-llm.py 2-1-2 --temperature 0.7
else
    echo "APIキーが設定されていないため、シミュレーションモードで実行します"
    python call-llm.py 2-1-2
fi

echo ""
echo "✅ テスト完了"