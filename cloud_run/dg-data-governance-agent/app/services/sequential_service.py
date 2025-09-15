"""
シーケンシャル実行サービス

データ品質シーケンシャル実行処理
"""

import logging
from typing import List
from typing import Tuple

from app.services.child_agent_service import ChildAgentService

logger = logging.getLogger(__name__)


class SequentialService:
    """シーケンシャル実行サービスクラス"""

    def __init__(self):
        """シーケンシャル実行サービス初期化"""
        self.child_agent_service = ChildAgentService()

    async def execute_data_quality_sequential(self, message: str, session_id: str, user_id: str, dataplex_url: str, bigquery_url: str) -> Tuple[str, List[str]]:
        """
        データ品質シーケンシャル実行（Google ADKベストプラクティス準拠）
        1. BigQueryエージェント: テーブル統計情報取得
        2. Dataplexエージェント: 統計情報に基づく品質ルール提案

        ADK Sequential Agent Pattern:
        - 厳密な処理順序の保証
        - 前のステップの出力が次のステップの入力になる依存関係
        - エラーハンドリングとロールバック対応

        Args:
            message: 送信するメッセージ
            session_id: セッションID
            dataplex_url: DataplexエージェントのURL
            bigquery_url: BigQueryエージェントのURL

        Returns:
            レスポンステキストと使用されたエージェントのリスト
        """
        logger.info(f"🔄 データ品質シーケンシャル実行開始: {message}")

        try:
            # フェーズ1: BigQueryエージェントでテーブル統計情報取得
            logger.info("📊 フェーズ1: BigQuery統計情報取得")
            bigquery_response, bigquery_agents = await self.child_agent_service.call_bigquery_agent(message, session_id, user_id, bigquery_url)

            if not bigquery_response:
                logger.error("BigQuery統計情報の取得に失敗")
                return "BigQuery統計情報の取得に失敗しました。", []

            # フェーズ2: Dataplexエージェントで品質ルール提案
            logger.info("🎯 フェーズ2: Dataplex品質ルール提案")

            # 統計情報に基づく品質ルール提案メッセージを準備
            has_statistics = "統計情報" in bigquery_response or "statistics" in bigquery_response.lower()
            if has_statistics:
                dataplex_message = f"{message}\n\n【BigQuery統計情報】\n{bigquery_response}\n\n上記の統計情報に基づいて、具体的なデータ品質ルールを提案してください。"
            else:
                dataplex_message = f"{message}\n\n【BigQuery分析結果】\n{bigquery_response}\n\nこの分析結果を踏まえて、データ品質ルールを提案してください。"

            dataplex_response, dataplex_agents = await self.child_agent_service.call_dataplex_agent(dataplex_message, session_id, user_id, dataplex_url)

            if not dataplex_response:
                logger.error("Dataplex品質ルール提案の取得に失敗")
                return f"{bigquery_response}\n\nDataplex品質ルール提案の取得に失敗しました。", bigquery_agents

            # 結果を統合
            combined_response = f"""
                ## 📊 BigQuery分析結果
                {bigquery_response}

                ## 🎯 Dataplex品質ルール提案
                {dataplex_response}

                ---
                *このレスポンスは、BigQuery統計情報取得 → Dataplex品質ルール提案のシーケンシャルワークフローで生成されました。*
            """
            combined_agents = bigquery_agents + dataplex_agents

            logger.info(f"✅ データ品質シーケンシャル実行完了: {len(combined_agents)}個のエージェント使用")
            return combined_response, combined_agents

        except Exception as e:
            logger.error(f"❌ シーケンシャル実行エラー: {e}")
            return f"データ品質シーケンシャル実行中にエラーが発生しました: {str(e)}", []
