# Dataplex データガバナンス Chat UI
FROM python:3.12-slim

# 環境変数の設定
ENV PYTHONPATH=/app
ENV GOOGLE_CLOUD_LOCATION=asia-northeast1
ENV CHAINLIT_HOST=0.0.0.0
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Poetry 2.1.1インストール
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry==2.1.1

# 依存関係設定ファイルをコピー
COPY pyproject.toml poetry.lock* ./

# Pythonパッケージをインストール
RUN poetry install --only main --no-interaction --no-ansi --no-root

# アプリケーションコードをコピー
COPY . .

# 非rootユーザーの作成と権限設定
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

# 非rootユーザーに切り替え
USER app

# ポートの公開
EXPOSE 8000

# Chainlitアプリケーション起動
CMD ["sh", "-c", "chainlit run app.py --host 0.0.0.0 --port ${PORT:-8000}"]
