"""
チャットAPI

データガバナンス親エージェントとのチャット機能
"""

import logging

from fastapi import APIRouter
from fastapi import HTTPException
from google.genai import types

from app.core import globals as g
from app.core.config import AgentConfig
from app.models import ChatRequest
from app.models import ChatResponse
from app.services.agent_routing_service import AgentRoutingService
from app.services.child_agent_service import ChildAgentService
from app.services.sequential_service import SequentialService

logger = logging.getLogger(__name__)

router = APIRouter()

# 設定とサービスインスタンス作成
config = AgentConfig()
config.load_environment_variables()
agent_routing_service = AgentRoutingService()
child_agent_service = ChildAgentService()
sequential_service = SequentialService()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """データガバナンス親エージェントとのチャットエンドポイント"""
    try:
        # ガード節：初期化状態チェック
        if not g.agent or not g.runner or not g.session_service:
            raise HTTPException(status_code=500, detail="Agent not initialized")

        session_id = request.session_id or "default"
        user_id = request.user_id or "unknown"
        logger.info(f"親エージェントチャットリクエスト: session_id={session_id}, message='{request.message[:100]}...'")

        # セッション存在確認と作成
        try:
            session = await g.session_service.get_session(app_name=AgentConfig.APP_NAME, user_id=user_id, session_id=session_id)
            if not session:
                # セッションが存在しない場合のみ作成
                await g.session_service.create_session(app_name=AgentConfig.APP_NAME, user_id=user_id, session_id=session_id)
                logger.info(f"新規セッション作成: {session_id}")
            else:
                logger.info(f"既存セッション使用: {session_id}")
        except Exception:
            # セッション取得失敗時は作成を試行
            try:
                await g.session_service.create_session(app_name=AgentConfig.APP_NAME, user_id=user_id, session_id=session_id)
                logger.info(f"セッション作成: {session_id}")
            except Exception as create_error:
                logger.error(f"セッション作成失敗: {create_error}")
                raise HTTPException(status_code=500, detail="セッション管理エラー")

        agents_used = []
        final_response = ""

        # ガバナンススコア関連の質問処理（最優先）
        if any(keyword in request.message.lower() for keyword in AgentConfig.GOVERNANCE_SCORE_KEYWORDS):
            logger.info("📊 ガバナンススコア関連の質問を検出、BigQueryエージェントに直接委譲")
            bigquery_response, bigquery_agents = await child_agent_service.call_bigquery_agent(request.message, session_id, user_id, config.bigquery_url)
            final_response = bigquery_response
            agents_used.extend(bigquery_agents)

        # データ品質シーケンシャル実行判定（BigQuery関連判定より優先）
        elif agent_routing_service.is_data_quality_sequential(request.message):
            logger.info("🔄 データ品質シーケンシャル実行を開始")
            final_response, agents_used = await sequential_service.execute_data_quality_sequential(request.message, session_id, user_id, config.dataplex_url, config.bigquery_url)

        # BigQuery関連の質問処理（共通設定を使用）
        elif agent_routing_service.is_bigquery_related(request.message):
            bigquery_response, bigquery_agents = await child_agent_service.call_bigquery_agent(request.message, session_id, user_id, config.bigquery_url)
            final_response = bigquery_response
            agents_used.extend(bigquery_agents)

        # データ品質ルール設定の質問処理（シーケンシャル実行以外）
        elif any(keyword in request.message.lower() for keyword in ["データ品質", "品質ルール", "品質チェック", "ガバナンス戦略", "data quality", "quality rule"]):
            # データ品質ルール設定は親エージェントが直接処理
            content = types.Content(role="user", parts=[types.Part(text=request.message)])
            governance_response = ""
            async for event in g.runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
                if event.is_final_response():
                    governance_response = event.content.parts[0].text
                    break
            final_response = governance_response
            agents_used.append("dg-data-governance-agent")

        # 親エージェントの処理（子エージェントの結果がない場合のみ）
        if not final_response:
            # 子エージェントの結果がない場合のみ親エージェントが処理
            message_to_process = request.message

            # あいまいなプロンプトの場合はセッション履歴を参照
            if agent_routing_service.is_ambiguous_prompt(request.message):
                logger.info("🔍 あいまいなプロンプトを検出、セッション履歴を参照")
                try:
                    session_context = await agent_routing_service.get_session_context(g.session_service, user_id, session_id)
                    message_to_process = f"{request.message}\n\n{session_context}"
                    agents_used.append("context-aware")
                except Exception as e:
                    logger.error(f"セッション履歴参照エラー: {e}")

            content = types.Content(role="user", parts=[types.Part(text=message_to_process)])
            governance_response = ""
            async for event in g.runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
                if event.is_final_response():
                    governance_response = event.content.parts[0].text
                    break
            final_response = governance_response

        # アイコンを動的に設定
        response_icon = "🤖"  # デフォルト（親エージェント）
        if "dg-dataplex-ai-agent" in agents_used:
            response_icon = "🏗️"  # Dataplexエージェント
        elif "dg-bigquery-ai-agent" in agents_used:
            response_icon = "📊"  # BigQueryエージェント
        elif "context-aware" in str(agents_used):
            response_icon = "🔍"  # コンテキスト考慮型

        logger.info(f"親エージェント処理完了: session_id={session_id}, agents_used={agents_used}, icon={response_icon}")

        return ChatResponse(response=final_response or "申し訳ありませんが、応答を生成できませんでした。", session_id=session_id, agents_used=agents_used, response_icon=response_icon)

    except Exception as e:
        logger.error(f"親エージェントチャット処理エラー: {e}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")
