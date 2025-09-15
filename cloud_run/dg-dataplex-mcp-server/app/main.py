import logging

from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

from app.api.dataplex import router as dataplex_router
from app.api.health import router as health_router
from app.core.config import get_settings

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 設定取得
settings = get_settings()

app = FastAPI(
    title="Data Management MCP Server",
    description="Dataplex API統合MCPサーバー - 非同期処理対応",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# APIルーター登録
app.include_router(health_router)
app.include_router(dataplex_router)

# FastAPI-MCP統合
mcp = FastApiMCP(app, name="dg-dataplex-mcp-server", description="Dataplex API統合MCPサーバー - AIエージェント連携")
mcp.mount()
