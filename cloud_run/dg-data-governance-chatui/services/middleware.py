"""
ミドルウェア

FastAPI/Chainlitアプリケーション用のカスタムミドルウェア
"""

import logging
from contextvars import ContextVar

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

# リクエストヘッダーを保存するContextVar
request_headers: ContextVar[dict[str, str]] = ContextVar("request_headers", default={})


class IAPHeaderMiddleware(BaseHTTPMiddleware):
    """IAPヘッダーを取得するミドルウェア"""

    async def dispatch(self, request: Request, call_next):
        """リクエスト処理とヘッダー取得"""
        # リクエストヘッダーをContextVarに保存
        headers = dict(request.headers)
        request_headers.set(headers)

        # 次の処理を実行
        response = await call_next(request)
        return response
