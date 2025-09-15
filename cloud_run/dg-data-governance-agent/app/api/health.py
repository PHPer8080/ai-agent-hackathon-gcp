"""
ヘルスチェックAPI

システムの健全性を確認するエンドポイント
"""

from fastapi import APIRouter

from app.core import globals as g
from app.core.config import AgentConfig
from app.models import HealthResponse

# 設定インスタンス作成
config = AgentConfig()
config.load_environment_variables()

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """ヘルスチェックエンドポイント"""
    return HealthResponse(
        status="healthy",
        service="dg-data-governance-agent",
        version="1.0.0",
        agent_status="ready" if g.agent else "not_initialized",
        child_agents_connected={
            "dg-dataplex-ai-agent": bool(config.dataplex_url),
            "dg-bigquery-ai-agent": bool(config.bigquery_url),
        },
    )
