"""
設定管理モジュール
環境変数とデフォルト設定の管理
"""

import os


class Settings:
    """アプリケーション設定"""

    def __init__(self) -> None:
        # Google Cloud設定
        self.project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")  # FIXME: プロジェクトIDを適宜変更
        self.location: str = os.getenv("GOOGLE_CLOUD_LOCATION", "asia-northeast1")

        # MCP設定
        self.mcp_server_name: str = os.getenv("MCP_SERVER_NAME", "dg-bigquery-mcp-server")

        # ログ設定
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"

        # BigQuery設定
        self.bigquery_default_dataset: str = os.getenv("BIGQUERY_DEFAULT_DATASET", "tt_hackathon")


def get_settings() -> Settings:
    """設定インスタンス取得"""
    return Settings()
