"""
チャット API エンドポイント
"""

import logging

from fastapi import APIRouter
from fastapi import HTTPException
from google.genai import types

from app.core import globals as g
from app.core.config import AgentConfig
from app.models.chat import ChatRequest
from app.models.chat import ChatResponse

logger = logging.getLogger(__name__)

config = AgentConfig()
config.load_environment_variables()
router = APIRouter(tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """統一エンドポイント：AIエージェントとのチャット（単体使用・A2A使用両対応）"""
    try:
        # 初期化状態チェック
        if not g.agent or not g.runner or not g.session_service:
            raise HTTPException(status_code=500, detail="Agent not initialized")

        session_id = request.session_id or "default"
        user_id = request.user_id or "unknown"
        logger.info(f"チャットリクエスト受信: user_id={user_id}, session_id={session_id}, message='{request.message[:100]}...'")

        # セッション存在確認と作成
        try:
            session = await g.session_service.get_session(app_name=config.APP_NAME, user_id=user_id, session_id=session_id)
            if not session:
                # セッションが存在しない場合のみ作成
                await g.session_service.create_session(app_name=config.APP_NAME, user_id=user_id, session_id=session_id)
                logger.info(f"新規セッション作成: {session_id}")
            else:
                logger.info(f"既存セッション使用: {session_id}")
                # セッション履歴の確認
                if hasattr(session, "messages") and session.messages:
                    logger.info(f"セッション履歴: {len(session.messages)}件のメッセージ")
                else:
                    logger.info("セッション履歴: なし")
        except Exception:
            # セッション取得失敗時は作成を試行
            try:
                await g.session_service.create_session(app_name=config.APP_NAME, user_id=user_id, session_id=session_id)
                logger.info(f"セッション作成: {session_id}")
            except Exception as create_error:
                logger.error(f"セッション作成失敗: {create_error}")
                raise HTTPException(status_code=500, detail="セッション管理エラー")

        # Google ADK async実行（types.Content形式）
        final_response = ""
        tools_used = []

        # mcp-database-frontendと同じContent形式に変換
        content = types.Content(role="user", parts=[types.Part(text=request.message)])

        async for event in g.runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
            if event.is_final_response():
                final_response = event.content.parts[0].text
                break
            elif event.content and event.content.parts:
                # ツール実行イベントを処理
                for part in event.content.parts:
                    if hasattr(part, "function_call") and part.function_call is not None:
                        tools_used.append(part.function_call.name)

        logger.info(f"AIエージェント応答完了: session_id={session_id}, tools_used={tools_used}")

        return ChatResponse(
            response=final_response or "申し訳ありませんが、応答を生成できませんでした。",
            session_id=session_id,
            tools_used=tools_used,
        )

    except Exception as e:
        logger.error(f"チャット処理エラー: {e}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")
