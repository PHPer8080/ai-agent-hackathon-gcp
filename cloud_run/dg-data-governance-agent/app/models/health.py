"""
ヘルスチェック関連のデータモデル
"""

from typing import Dict

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """ヘルスチェックレスポンスモデル"""

    status: str
    service: str
    version: str
    agent_status: str
    child_agents_connected: Dict[str, bool]
