FROM python:3.12-slim

# 環境変数の設定
ENV PYTHONPATH=/app
ENV ADK_DEBUG=1
ENV GOOGLE_GENAI_USE_VERTEXAI=TRUE
ENV GOOGLE_CLOUD_LOCATION=asia-northeast1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Poetry 2.1.1インストール
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry==2.1.1

# 依存関係設定ファイルをコピー
COPY pyproject.toml poetry.lock* ./

# Pythonパッケージをインストール
RUN poetry install --only main --no-interaction --no-ansi --no-root

# アプリケーションコード
COPY . .

# 必要なディレクトリを作成
RUN mkdir -p agent/eval_sets && \
    echo "[]" > agent/eval_sets/empty_eval_set.json

# 非rootユーザーの作成と権限設定
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

# 非rootユーザーに切り替え
USER app

# ポートの公開
EXPOSE 8080

# アプリケーションの起動（環境に応じて自動切り替え）
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
