import logging
import os
import uuid

import chainlit as cl
import chainlit.server

from services.auth_service import AuthService
from services.chat_client_service import ChatClientService
from services.middleware import IAPHeaderMiddleware

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ChainlitのFastAPIアプリにミドルウェアを追加
if hasattr(chainlit.server, "app"):
    chainlit.server.app.add_middleware(IAPHeaderMiddleware)
    logger.info("IAPHeaderMiddleware追加完了")

# 認証サービス初期化
auth_service = AuthService()

chat_client_service = ChatClientService(os.getenv("AGENT_URL"))


@cl.on_chat_start
async def start():
    """チャット開始時の初期化"""
    # IAP認証されたユーザー情報を取得
    user_id = auth_service.get_user_email()

    # セッション情報を設定
    cl.user_session.set("user_id", user_id)
    cl.user_session.set("session_id", str(uuid.uuid4()))

    if auth_service.is_authenticated():
        logger.info("ユーザー認証成功")
    else:
        logger.warning("ユーザー認証失敗")

    # データガバナンス関連のプリセットプロンプト用のアクション
    actions = [
        # BigQueryエージェント機能
        cl.Action(
            name="preset_datasets",
            value="your-project-idプロジェクトのBigQueryデータセット一覧を表示して",  # FIXME: プロジェクトIDを適宜変更
            label="📊 データセット一覧",
        ),
        cl.Action(
            name="preset_lineage",
            value="tt_usデータセットのproduct_catalogテーブルの依存関係（リネージ）を分析して",
            label="🔗 データ系譜分析",
        ),
        cl.Action(
            name="preset_governance_score",
            value="tt_usデータセットのcustomer_profilesテーブルのガバナンススコアを計算して評価して",
            label="📈 ガバナンススコア",
        ),
        cl.Action(
            name="preset_missing_metadata",
            value="tt_usデータセットで説明や論理名が不足しているテーブルを検出して",
            label="🏷️ メタデータ不足検出",
        ),
        cl.Action(
            name="preset_column_info",
            value="tt_usデータセットのorder_detailsテーブルのカラム情報と説明を確認して",
            label="📋 カラム情報確認",
        ),
        cl.Action(
            name="preset_statistics",
            value="tt_usデータセットのraw_ordersテーブルの統計情報を取得してデータ品質を分析して",
            label="📊 統計情報分析",
        ),
        # Dataplexエージェント機能
        cl.Action(
            name="preset_quality_rules",
            value="tt_usデータセットのproduct_catalogテーブルについて、BigQuery統計情報に基づいてデータ品質ルールを提案して",
            label="🛡️ 品質ルール提案",
        ),
        cl.Action(
            name="preset_metadata_suggest",
            value="tt_usデータセットのraw_customersテーブルの論理名と説明を提案して",
            label="💡 メタデータ提案",
        ),
    ]

    # ユーザー情報を含むウェルカムメッセージ
    user_display = user_id if user_id else "unknown"
    welcome_message = (
        f"🛡️ **データガバナンス統合アシスタント**\n\n"
        f"こんにちは、{user_display}さん！\n\n"
        "BigQueryメタデータ管理とDataplex品質管理を統合したAIアシスタントです。\n\n"
        "**🔧 利用可能な機能**:\n"
        "• **BigQueryエージェント**: データセット一覧、テーブル系譜、ガバナンススコア、統計情報分析\n"
        "• **Dataplexエージェント**: データ品質ルール提案、メタデータ改善提案\n\n"
        "下のボタンから選択するか、自由にメッセージを入力してください！\n"
        "例: 「tt_usデータセットのテーブル一覧を表示して」「tt_usデータセットのproduct_catalogテーブルの品質ルールを提案して」"
    )
    await cl.Message(content=welcome_message, actions=actions).send()


@cl.action_callback("preset_datasets")
@cl.action_callback("preset_lineage")
@cl.action_callback("preset_governance_score")
@cl.action_callback("preset_missing_metadata")
@cl.action_callback("preset_column_info")
@cl.action_callback("preset_statistics")
@cl.action_callback("preset_quality_rules")
@cl.action_callback("preset_metadata_suggest")
async def on_action(action: cl.Action):
    """クイックアクションボタンがクリックされた時の処理"""
    session_id = cl.user_session.get("session_id", "default")
    user_id = cl.user_session.get("user_id", "unknown")
    prompt = action.value

    logger.info(f"アクション実行: {action.name}, user_authenticated={bool(user_id)}")

    # ユーザーが選択したプロンプトを表示
    await cl.Message(content=f"📝 実行プロンプト: {prompt}").send()

    # 処理中メッセージ
    processing_msg = cl.Message(content="🔍 分析中...")
    await processing_msg.send()

    try:
        await chat_client_service.send_message(prompt, session_id, user_id)
    except Exception as e:
        logger.error(f"アクション実行エラー: {e}")
        await cl.Message(content="❌ エラーが発生しました").send()
    finally:
        await processing_msg.remove()


@cl.on_message
async def main(message: cl.Message):
    """メッセージ受信時の処理"""
    session_id = cl.user_session.get("session_id", "default")
    user_id = cl.user_session.get("user_id", "unknown")
    processing_msg = cl.Message(content="🔍 分析中...")
    await processing_msg.send()

    try:
        await chat_client_service.send_message(message.content, session_id, user_id)
    except Exception as e:
        logger.error(f"メッセージ処理エラー: {e}")
        await cl.Message(content="❌ エラーが発生しました").send()
    finally:
        await processing_msg.remove()
