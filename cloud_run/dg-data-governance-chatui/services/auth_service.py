"""
認証サービス

Identity-Aware Proxy認証後のユーザー情報取得処理
Cloud Run間通信用の認証トークン管理
"""

import logging
import os
from typing import Optional

import requests

from services.middleware import request_headers

logger = logging.getLogger(__name__)


class AuthService:
    """IAP認証サービスクラス"""

    def __init__(self):
        """認証サービス初期化"""
        self.is_development = os.getenv("CHAINLIT_ENV", "production") == "development"
        self.identity_token: Optional[str] = None

    def get_user_email(self) -> Optional[str]:
        """
        IAP認証されたユーザーメールを取得

        Returns:
            ユーザーメールアドレス、取得失敗時はNone
        """
        headers = request_headers.get({})

        # IAPヘッダーからUser Emailを取得（大文字小文字を考慮）
        user_email = headers.get("x-goog-authenticated-user-email") or headers.get("X-Goog-Authenticated-User-Email")

        # 開発環境用のフォールバック
        if not user_email and self.is_development:
            logger.info("開発環境: モックユーザーメールを使用")
            return "developer@example.com"

        # ヘッダー値をクリーンアップ
        if user_email:
            cleaned_email = user_email.replace("accounts.google.com:", "").strip()
            logger.info("IAP認証ユーザーメール取得成功")
            return cleaned_email

        logger.warning("IAP認証ユーザーメールが取得できませんでした")
        return None

    def is_authenticated(self) -> bool:
        """
        認証状態を確認

        Returns:
            認証済みの場合True、未認証の場合False
        """
        return self.get_user_email() is not None

    def get_identity_token(self, audience: str) -> Optional[str]:
        """
        Cloud Runメタデータサーバーから認証トークンを取得

        Args:
            audience: トークンの対象となるサービスURL

        Returns:
            認証トークン、取得失敗時はNone
        """
        metadata_server_url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity"
        headers = {"Metadata-Flavor": "Google"}
        params = {"audience": audience, "format": "full"}

        try:
            response = requests.get(metadata_server_url, headers=headers, params=params, timeout=10)
            if response.status_code != 200:
                logger.warning(f"認証トークン取得失敗: HTTP {response.status_code}")
                return None

            token = response.text.strip()
            logger.info("認証トークン取得成功")
            return token
        except Exception as e:
            logger.warning(f"認証トークン取得エラー: {e}")
            return None

    def refresh_token(self, audience: str):
        """
        認証トークンを更新

        Args:
            audience: トークンの対象となるサービスURL
        """
        self.identity_token = self.get_identity_token(audience)
        if not self.identity_token:
            logger.warning("認証トークンの更新に失敗しました")

    def get_auth_headers(self) -> dict[str, str]:
        """
        認証ヘッダーを取得

        Returns:
            認証ヘッダー辞書
        """
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.identity_token:
            headers["Authorization"] = f"Bearer {self.identity_token}"
        return headers
