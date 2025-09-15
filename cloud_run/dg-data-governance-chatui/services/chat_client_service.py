import asyncio
import logging

import aiohttp
import chainlit as cl

from services.auth_service import AuthService

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatClientService:
    """チャットエージェントとの通信を管理するサービス"""

    def __init__(self, agent_url: str):
        self.agent_url = agent_url
        self.auth_service = AuthService()
        self.auth_service.refresh_token(agent_url)

    async def send_message(self, message: str, session_id: str, user_id: str = None) -> None:
        """チャットエージェントにメッセージを送信して表示"""
        try:
            url = f"{self.agent_url}/chat"
            payload = {"message": message, "session_id": session_id, "user_id": user_id}

            async with aiohttp.ClientSession() as session:
                timeout = aiohttp.ClientTimeout(total=120)
                headers = self.auth_service.get_auth_headers()
                async with session.post(url, json=payload, headers=headers, timeout=timeout) as response:
                    # early return for success
                    if response.status == 200:
                        result = await response.json()
                        response_text = result.get("response", "応答を取得できませんでした")
                        await cl.Message(content=response_text).send()
                        return

                    # early return for auth error
                    if response.status == 401:
                        self._refresh_token()
                        await self.send_message(message, session_id)
                        return

                    # other errors
                    logger.error(f"エラー応答: {response.status}")
                    await cl.Message(content="エラーが発生しました。しばらく待ってから再試行してください。").send()
        except asyncio.TimeoutError:
            await cl.Message(content="リクエストがタイムアウトしました。しばらく待ってから再試行してください。").send()
        except Exception as e:
            logger.error(f"通信エラー: {e}")
            await cl.Message(content="通信エラーが発生しました。しばらく待ってから再試行してください。").send()
