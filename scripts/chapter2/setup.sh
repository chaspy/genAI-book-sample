#!/bin/bash

# 第2章サンプルコード環境構築スクリプト
# 複数の環境構築方法から選択できます

set -e

echo "==================================="
echo "第2章 Prompt Engineering"
echo "環境構築セットアップ"
echo "==================================="
echo ""

# Pythonバージョンチェック
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d " " -f 2)
        echo "✅ Python $PYTHON_VERSION が見つかりました"
        
        # バージョン確認（3.10以上が必要）
        MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        
        if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 10 ]); then
            echo "⚠️ Python 3.10以上が必要です"
            return 1
        fi
        return 0
    else
        echo "❌ Python3が見つかりません"
        return 1
    fi
}

# 環境構築方法の選択
echo "環境構築方法を選択してください:"
echo "1) uv (推奨・高速)"
echo "2) pip + venv (標準)"
echo "3) Docker (完全分離環境)"
echo "4) 手動セットアップの手順を表示"
echo ""
read -p "選択 [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "📦 uvでの環境構築を開始..."
        
        # uvのインストール確認
        if ! command -v uv &> /dev/null; then
            echo "uvをインストールしています..."
            curl -LsSf https://astral.sh/uv/install.sh | sh
            export PATH="$HOME/.cargo/bin:$PATH"
        fi
        
        # uvで依存関係をインストール
        echo "依存関係をインストール中..."
        uv pip sync pyproject.toml
        uv venv
        
        echo ""
        echo "✅ uv環境構築完了！"
        echo ""
        echo "実行方法:"
        echo "  source .venv/bin/activate"
        echo "  cp .env.example .env"
        echo "  # .envファイルにAPIキーを設定"
        echo "  python 2-1-2_temperature_demo.py --demo"
        ;;
        
    2)
        echo ""
        echo "📦 pip + venvでの環境構築を開始..."
        
        if ! check_python; then
            echo "Python 3.10以上をインストールしてください"
            exit 1
        fi
        
        # venv作成
        echo "仮想環境を作成中..."
        python3 -m venv .venv
        
        # アクティベート
        source .venv/bin/activate
        
        # pipアップグレード
        pip install --upgrade pip
        
        # 依存関係インストール
        echo "依存関係をインストール中..."
        pip install -r requirements.txt
        
        echo ""
        echo "✅ venv環境構築完了！"
        echo ""
        echo "実行方法:"
        echo "  source .venv/bin/activate"
        echo "  cp .env.example .env"
        echo "  # .envファイルにAPIキーを設定"
        echo "  python 2-1-2_temperature_demo.py --demo"
        ;;
        
    3)
        echo ""
        echo "🐳 Dockerでの環境構築..."
        
        if ! command -v docker &> /dev/null; then
            echo "❌ Dockerがインストールされていません"
            echo "https://docs.docker.com/get-docker/ からインストールしてください"
            exit 1
        fi
        
        echo "Dockerイメージをビルド中..."
        docker build -t genai-book-chapter2 .
        
        echo ""
        echo "✅ Dockerイメージ構築完了！"
        echo ""
        echo "実行方法:"
        echo "  cp .env.example .env"
        echo "  # .envファイルにAPIキーを設定"
        echo "  docker run --rm -it --env-file .env genai-book-chapter2 python 2-1-2_temperature_demo.py --demo"
        ;;
        
    4)
        echo ""
        echo "📋 手動セットアップ手順"
        echo ""
        echo "1. Python 3.10以上をインストール"
        echo "   - pyenv: https://github.com/pyenv/pyenv"
        echo "   - 公式: https://www.python.org/downloads/"
        echo ""
        echo "2. 以下のパッケージをインストール:"
        echo "   pip install openai==2.6.1"
        echo "   pip install tiktoken==0.12.0"
        echo "   pip install python-dotenv==1.2.1"
        echo ""
        echo "3. 環境変数を設定:"
        echo "   cp .env.example .env"
        echo "   # .envファイルを編集してAPIキーを設定"
        echo ""
        echo "4. スクリプトを実行:"
        echo "   python 2-1-2_temperature_demo.py --demo"
        ;;
        
    *)
        echo "無効な選択です"
        exit 1
        ;;
esac

echo ""
echo "================================"
echo "セットアップに関する詳細は README.md を参照してください"
echo "================================"