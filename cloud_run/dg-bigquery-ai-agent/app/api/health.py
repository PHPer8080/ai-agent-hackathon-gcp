"""
ヘルスチェック API エンドポイント
"""

from fastapi import APIRouter

from app.core import globals as g
from app.core.config import AgentConfig
from app.models.health import HealthResponse

config = AgentConfig()
config.load_environment_variables()
router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """ヘルスチェックエンドポイント（軽量・高速）"""
    return HealthResponse(
        status="healthy",
        service="dg-bigquery-ai-agent",
        version="1.0.0",
        agent_status="ready" if g.agent else "not_initialized",
        mcp_server_connected=bool(config.mcp_server_url),
    )
