# Python 3.12 slim image
FROM python:3.12-slim

# 環境変数設定（FROMの直後）
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONPATH=/app

WORKDIR /app

# 非rootユーザー作成
RUN groupadd --gid 1000 app && \
    useradd --uid 1000 --gid app --shell /bin/bash --create-home app

# Poetry 2.1.1インストール
RUN pip install --upgrade pip && \
    pip install poetry==2.1.1

# poetry.lockファイルを使用した依存関係管理
COPY pyproject.toml poetry.lock* ./
RUN poetry install --only main --no-interaction --no-ansi --no-root

# アプリケーションコード
COPY . .
RUN chown -R app:app /app
USER app

# Cloud Runポート設定
EXPOSE $PORT

# アプリケーション起動
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
