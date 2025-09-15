"""
認証サービス

Cloud Run Identity Token取得処理
"""

import logging
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class AuthService:
    """認証サービスクラス"""

    def __init__(self):
        """認証サービス初期化"""
        self.metadata_server_url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity"
        self.headers = {"Metadata-Flavor": "Google"}
        self.timeout = 10

    def get_identity_token(self, audience: str) -> Optional[str]:
        """
        Cloud Run メタデータサーバーからIdentity Tokenを取得

        Args:
            audience: トークンの対象オーディエンス

        Returns:
            Identity Token文字列、取得失敗時はNone
        """
        params = {"audience": audience, "format": "full"}

        try:
            response = requests.get(self.metadata_server_url, headers=self.headers, params=params, timeout=self.timeout)
            if response.status_code != 200:
                logger.error(f"Identity token取得失敗: {response.status_code}")
                return None
            return response.text.strip()
        except Exception as e:
            logger.error(f"Identity token取得エラー: {e}")
            return None
