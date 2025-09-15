"""
チャット関連のデータモデル
"""

from typing import List
from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """チャットリクエストモデル"""

    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None


class ChatResponse(BaseModel):
    """チャットレスポンスモデル"""

    response: str
    session_id: str
    tools_used: List[str] = []
