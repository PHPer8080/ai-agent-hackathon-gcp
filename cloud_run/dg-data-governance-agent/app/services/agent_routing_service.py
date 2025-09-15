"""
データガバナンスエージェント共通サービス

エージェント間で共有される処理ロジックを管理
"""

import logging

from app.core.config import AgentConfig

logger = logging.getLogger(__name__)


class AgentRoutingService:
    """エージェントルーティングサービスクラス"""

    def __init__(self):
        """エージェントルーティングサービス初期化"""
        pass

    def is_bigquery_related(self, message: str) -> bool:
        """
        BigQuery関連の質問かどうかを判定

        Args:
            message: 判定対象のメッセージ

        Returns:
            bool: BigQuery関連の場合True、Dataplex専用の場合False
        """
        message_lower = message.lower()

        # Dataplex専用の場合は除外
        if any(keyword in message_lower for keyword in AgentConfig.DATAPLEX_KEYWORDS):
            return False

        # 明確なBigQueryキーワードがある場合
        if any(keyword in message_lower for keyword in AgentConfig.BIGQUERY_EXPLICIT_KEYWORDS):
            return True

        # プロジェクト・データセット名がある場合
        if any(keyword in message_lower for keyword in AgentConfig.PROJECT_KEYWORDS):
            return True

        # データ関連 + 操作キーワードの組み合わせ
        has_data = any(keyword in message_lower for keyword in AgentConfig.DATA_KEYWORDS)
        has_action = any(keyword in message_lower for keyword in AgentConfig.ACTION_KEYWORDS)
        has_governance = any(keyword in message_lower for keyword in AgentConfig.GOVERNANCE_KEYWORDS)

        if has_data and (has_action or has_governance):
            return True

        # ガバナンス関連の質問
        if has_governance and ("不足" in message_lower or "ない" in message_lower or "設定" in message_lower):
            return True

        return False

    def is_dataplex_related(self, message: str) -> bool:
        """
        Dataplex関連の質問かどうかを判定

        Args:
            message: 判定対象のメッセージ

        Returns:
            bool: Dataplex関連の場合True
        """
        message_lower = message.lower()

        # Dataplex専用キーワードがある場合
        return any(keyword in message_lower for keyword in AgentConfig.DATAPLEX_KEYWORDS)

    def is_data_quality_sequential(self, message: str) -> bool:
        """
        データ品質シーケンシャル実行が必要かどうかを判定
        BigQuery統計情報取得 → Dataplex品質ルール提案の流れ

        Args:
            message: 判定対象のメッセージ

        Returns:
            bool: シーケンシャル実行が必要な場合True
        """
        message_lower = message.lower()

        # データ品質シーケンシャル実行キーワードがある場合
        return any(keyword in message_lower for keyword in AgentConfig.DATA_QUALITY_SEQUENTIAL_KEYWORDS)

    def is_ambiguous_prompt(self, message: str) -> bool:
        """
        あいまいなプロンプトかどうかを判定

        Args:
            message: 判定対象のメッセージ

        Returns:
            bool: あいまいなプロンプトの場合True
        """
        message_lower = message.lower().strip()

        # 短すぎるメッセージ（5文字以下）
        if len(message_lower) <= 5:
            return True

        # 代名詞や指示語が含まれている
        if any(keyword in message_lower for keyword in AgentConfig.AMBIGUOUS_QUESTION_WORDS):
            return True

        # 疑問符のみ、または非常に短い疑問文
        if message_lower in AgentConfig.AMBIGUOUS_SHORT_QUESTIONS:
            return True

        # 単語数が少ない（3単語以下）
        words = message_lower.split()
        if len(words) <= 3:
            return True

        return False

    async def get_session_context(self, session_service, user_id: str, session_id: str, limit: int = 5) -> str:
        """
        セッション履歴から関連するコンテキストを取得

        Args:
            session_service: セッションサービスインスタンス
            user_id: ユーザーID
            session_id: セッションID
            limit: 取得する履歴の最大数

        Returns:
            str: 関連するコンテキスト情報
        """
        try:
            # セッション履歴を取得
            session = await session_service.get_session("app_name", user_id, session_id)
            if not session or not hasattr(session, "messages") or not session.messages:
                return "セッション履歴が見つかりません。"

            # 最新の会話履歴を取得（limit件まで）
            recent_messages = session.messages[-limit * 2 :] if len(session.messages) > limit * 2 else session.messages

            # ユーザーメッセージとアシスタント応答のペアを構築
            context_pairs = []
            for i in range(0, len(recent_messages) - 1, 2):
                if i + 1 < len(recent_messages):
                    user_msg = recent_messages[i]
                    assistant_msg = recent_messages[i + 1]

                    # メッセージの内容を抽出
                    user_content = ""
                    assistant_content = ""

                    if hasattr(user_msg, "parts") and user_msg.parts:
                        user_content = user_msg.parts[0].text if user_msg.parts[0].text else ""
                    elif hasattr(user_msg, "content"):
                        user_content = str(user_msg.content)

                    if hasattr(assistant_msg, "parts") and assistant_msg.parts:
                        assistant_content = assistant_msg.parts[0].text if assistant_msg.parts[0].text else ""
                    elif hasattr(assistant_msg, "content"):
                        assistant_content = str(assistant_msg.content)

                    if user_content and assistant_content:
                        # 長すぎる応答は要約
                        if len(assistant_content) > 200:
                            assistant_content = assistant_content[:200] + "..."

                        context_pairs.append(f"ユーザー: {user_content}\nアシスタント: {assistant_content}")

            if not context_pairs:
                return "関連する会話履歴が見つかりません。"

            # コンテキストを構築
            context = "【直近の会話履歴】\n" + "\n\n".join(context_pairs[-3:])  # 最新3件
            return context

        except Exception as e:
            logger.error(f"セッション履歴の取得中にエラーが発生: {e}")
            return f"セッション履歴の取得中にエラーが発生しました: {str(e)}"
