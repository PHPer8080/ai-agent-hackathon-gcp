"""
ヘルスチェック関連のデータモデル
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """ヘルスチェックレスポンスモデル"""

    status: str
    service: str
    version: str
    agent_status: str
    mcp_server_connected: bool
