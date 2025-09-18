FROM python:3.12-slim

# 環境変数設定（FROMの直後）
ENV PYTHONPATH=/app
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Poetry 2.1.1インストール
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry==2.1.1

# poetry.lockファイルを使用した依存関係管理
COPY pyproject.toml poetry.lock* ./

# Pythonパッケージをインストール
RUN poetry install --only main --no-interaction --no-ansi --no-root

# アプリケーションコード
COPY . .

# 非rootユーザーの作成と権限設定
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

# 非rootユーザーに切り替え
USER app

# ポート公開（Cloud RunのPORT環境変数を使用）
EXPOSE 8080

# FastAPIアプリケーション起動（タイムアウト設定追加）
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080} --timeout-keep-alive 300 --timeout-graceful-shutdown 30"]
