"""
ヘルスチェック API エンドポイント
"""

from typing import Any
from typing import Dict

from fastapi import APIRouter

# APIルーター
router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """ヘルスチェックエンドポイント"""
    return {
        "status": "healthy",
        "service": "dg-bigquery-mcp-server",
        "version": "1.0.0",
        "message": "BigQuery MCP Server is running",
    }
