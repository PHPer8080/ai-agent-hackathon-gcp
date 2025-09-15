"""
初期化サービス

Google ADK エージェント・ランナー・セッションサービスの初期化
"""

import logging
from typing import Tuple

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import FunctionTool

from app.core.config import AgentConfig
from app.services.bigquery_service import BigQueryService

logger = logging.getLogger(__name__)


class InitializationService:
    """初期化サービス"""

    def __init__(self):
        self.config = AgentConfig()
        self.bigquery_service = BigQueryService()
        self.agent = None
        self.runner = None
        self.session_service = None

    def initialize_all(self, app_name: str) -> Tuple[LlmAgent, Runner, InMemorySessionService]:
        """
        全コンポーネントの初期化

        Args:
            app_name: アプリケーション名

        Returns:
            agent, runner, session_service のタプル

        Raises:
            RuntimeError: 初期化に失敗した場合
        """
        try:
            # 設定読み込み
            self.config.load_environment_variables()

            # セッション管理初期化
            self.session_service = InMemorySessionService()
            logger.info("InMemorySessionService初期化完了（必須）")

            # エージェント初期化
            self.agent = self._create_agent()
            logger.info("LlmAgent初期化完了")

            # Runner初期化
            self.runner = self._create_runner(app_name)
            logger.info("Runner初期化完了（session_service必須）")

            # 初期化完了ログ
            logger.info(self.config.get_status_summary())

            return (self.agent, self.runner, self.session_service)

        except Exception as e:
            logger.error(f"初期化エラー: {e}")
            raise RuntimeError(f"Agent初期化に失敗しました: {e}")

    def _create_agent(self) -> LlmAgent:
        """
        BigQuery AIエージェントの作成

        Returns:
            初期化されたLlmAgent
        """
        # AIエージェントの指示を設定から取得
        instruction = self.config.get_agent_instruction()

        # BigQuery API ツールの作成
        bigquery_tools = []
        if self.config.mcp_server_url:
            bigquery_tools = [
                FunctionTool(self.bigquery_service.get_bigquery_datasets),
                FunctionTool(self.bigquery_service.get_table_lineage),
                FunctionTool(self.bigquery_service.find_tables_missing_description),
                FunctionTool(self.bigquery_service.find_tables_missing_logical_name),
                FunctionTool(self.bigquery_service.suggest_logical_name),
                FunctionTool(self.bigquery_service.suggest_description),
                FunctionTool(self.bigquery_service.check_column_descriptions),
                FunctionTool(self.bigquery_service.calculate_governance_score),
                FunctionTool(self.bigquery_service.get_table_statistics),
            ]
            logger.info(f"BigQuery FunctionTool を作成: {len(bigquery_tools)}個")

        return LlmAgent(
            name="dg_bigquery_assistant",
            model=self.config.MODEL_NAME,
            instruction=instruction,
            description="Google Cloud BigQueryデータアシスタント（ガードレール機能付き）",
            tools=bigquery_tools,
            before_tool_callback=self.bigquery_service.combined_guardrail_callback,  # 🛡️ ガードレール設定
        )

    def _create_runner(self, app_name: str) -> Runner:
        """
        Runnerの作成

        Args:
            app_name: アプリケーション名

        Returns:
            初期化されたRunner
        """
        if not self.agent or not self.session_service:
            raise RuntimeError("Agent または SessionService が初期化されていません")

        return Runner(agent=self.agent, app_name=app_name, session_service=self.session_service)
