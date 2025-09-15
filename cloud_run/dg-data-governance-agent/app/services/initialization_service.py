"""
初期化サービス

Google ADK エージェント・ランナー・セッションサービスの初期化
"""

import logging
from typing import Tuple

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from app.core.config import AgentConfig

logger = logging.getLogger(__name__)


class InitializationService:
    """初期化サービス"""

    def __init__(self):
        self.config = AgentConfig()
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
            logger.info("InMemorySessionService初期化完了")

            # エージェント初期化
            self.agent = self._create_agent()
            logger.info("親エージェント初期化完了")

            # Runner初期化
            self.runner = self._create_runner(app_name)
            logger.info("Runner初期化完了")

            # 初期化完了ログ
            logger.info(self.config.get_status_summary())

            return (self.agent, self.runner, self.session_service)

        except Exception as e:
            logger.error(f"初期化エラー: {e}")
            raise RuntimeError(f"Agent初期化に失敗しました: {e}")

    def _create_agent(self) -> LlmAgent:
        """
        親エージェントの作成

        Returns:
            初期化されたLlmAgent
        """
        instruction = self.config.get_agent_instruction()

        return LlmAgent(
            name="dg_data_governance_coordinator",
            model="gemini-1.5-flash",  # 軽量モデルを使用
            instruction=instruction,
            description="データガバナンス戦略立案・調整エージェント",
            tools=[],  # 必要最小限：ツールなし
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
