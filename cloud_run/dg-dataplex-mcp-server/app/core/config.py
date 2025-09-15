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
        self.location: str = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

        # MCP設定
        self.mcp_server_name: str = os.getenv("MCP_SERVER_NAME", "dg-dataplex-mcp-server")

        # ログ設定
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"

        # Dataplex設定
        self.dataplex_default_lake: str = os.getenv("DATAPLEX_DEFAULT_LAKE", "")
        self.dataplex_default_zone: str = os.getenv("DATAPLEX_DEFAULT_ZONE", "")


def get_settings() -> Settings:
    """設定インスタンス取得"""
    return Settings()
