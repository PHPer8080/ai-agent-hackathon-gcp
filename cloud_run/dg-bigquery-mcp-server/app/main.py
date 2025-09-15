import logging

from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

from app.api.bigquery import router as bigquery_router
from app.api.health import router as health_router
from app.core.config import get_settings

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 設定取得
settings = get_settings()

app = FastAPI(
    title="BigQuery MCP Server",
    description="BigQuery専用MCPサーバー - データガバナンス機能",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# APIルーター登録
app.include_router(health_router)
app.include_router(bigquery_router)

# FastAPI-MCP統合
mcp = FastApiMCP(app, name="dg-bigquery-mcp-server", description="BigQuery専用MCPサーバー - データガバナンス機能")
mcp.mount()
