"""
子エージェント呼び出しサービス

Dataplex・BigQueryエージェントとの通信処理
"""

import logging
from typing import List
from typing import Tuple

import httpx

from app.services.auth_service import AuthService

logger = logging.getLogger(__name__)


class ChildAgentService:
    """子エージェント呼び出しサービスクラス"""

    def __init__(self):
        """子エージェントサービス初期化"""
        self.auth_service = AuthService()
        self.timeout = 60.0

    async def call_dataplex_agent(self, message: str, session_id: str, user_id: str, dataplex_url: str) -> Tuple[str, List[str]]:
        """
        Dataplex専門エージェントを呼び出し

        Args:
            message: 送信するメッセージ
            session_id: セッションID
            dataplex_url: DataplexエージェントのURL

        Returns:
            レスポンステキストと使用されたエージェントのリスト
        """
        # ガード節：URL設定チェック
        if not dataplex_url:
            logger.warning("Dataplex URL未設定")
            return "", []

        # ガード節：認証トークン取得
        token = self.auth_service.get_identity_token(dataplex_url)
        if not token:
            logger.error("認証トークンの取得に失敗しました")
            return "", []

        logger.info("Dataplex専門エージェントに委譲")

        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        chat_payload = {"message": message, "session_id": session_id, "user_id": user_id}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(f"{dataplex_url}/chat", json=chat_payload, headers=headers)

                if response.status_code != 200:
                    logger.error(f"Dataplexエージェント呼び出し失敗: {response.status_code}")
                    return "", []

                chat_result = response.json()
                return chat_result.get("response", ""), chat_result.get("agents_used", [])

        except Exception as e:
            logger.error(f"Dataplexエージェント通信エラー: {e}")
            return "", []

    async def call_bigquery_agent(self, message: str, session_id: str, user_id: str, bigquery_url: str) -> Tuple[str, List[str]]:
        """
        BigQuery専門エージェントを呼び出し

        Args:
            message: 送信するメッセージ
            session_id: セッションID
            bigquery_url: BigQueryエージェントのURL

        Returns:
            レスポンステキストと使用されたエージェントのリスト
        """
        # ガード節：URL設定チェック
        if not bigquery_url:
            logger.warning("BigQuery URL未設定")
            return "", []

        # ガード節：認証トークン取得
        token = self.auth_service.get_identity_token(bigquery_url)
        if not token:
            logger.error("認証トークンの取得に失敗しました")
            return "", []

        logger.info("BigQuery専門エージェントに委譲")

        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        chat_payload = {"message": message, "session_id": session_id, "user_id": user_id}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(f"{bigquery_url}/chat", json=chat_payload, headers=headers)

                if response.status_code != 200:
                    logger.error(f"BigQueryエージェント呼び出し失敗: {response.status_code}")
                    return "", []

                chat_result = response.json()
                response_text = f"**BigQuery分析結果**:\n{chat_result.get('response', 'データなし')}\n\n"
                agents_used = ["dg-bigquery-ai-agent"]

                return response_text, agents_used

        except Exception as e:
            logger.error(f"BigQueryエージェント通信エラー: {e}")
            return "", []
