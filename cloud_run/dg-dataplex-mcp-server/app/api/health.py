"""
ヘルスチェック API エンドポイント
"""

from typing import Any
from typing import Dict

from fastapi import APIRouter

from app.core.config import get_settings

settings = get_settings()

# APIルーター
router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """メインヘルスチェックエンドポイント"""
    return {
        "status": "healthy",
        "service": "dg-dataplex-mcp-server",
        "version": "1.0.0",
        "project_id": settings.project_id,
        "location": settings.location,
        "dataplex_ready": True,
    }
