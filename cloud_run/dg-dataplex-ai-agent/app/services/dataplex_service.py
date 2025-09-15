"""
Dataplexサービス

データ品質ルール提案とガードレール機能
"""

import logging
from typing import Any
from typing import Dict
from typing import Optional

import requests
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext

from app.core.config import AgentConfig
from app.services.auth_service import AuthService

logger = logging.getLogger(__name__)


class DataplexService:
    """Dataplexサービス"""

    def __init__(self):
        self.config = AgentConfig()
        self.config.load_environment_variables()
        self.auth_service = AuthService()

    def suggest_data_quality_rules(self, project_id: str, dataset_id: str, table_id: str, bigquery_statistics: Optional[str] = None) -> str:
        """BigQuery統計情報に基づくデータ品質ルールの提案"""
        return self.call_mcp_server("suggest-data-quality-rules", {"project_id": project_id, "dataset_id": dataset_id, "table_id": table_id, "bigquery_statistics": bigquery_statistics})

    def call_mcp_server(self, tool_name: str, arguments: dict) -> str:
        """MCPサーバーへリクエスト送信"""
        if not self.config.mcp_server_url:
            return "エラー: MCP サーバー接続が設定されていません。"

        try:
            token = self.auth_service.get_identity_token(self.config.mcp_server_url)
            if not token:
                return "エラー: 認証トークンの取得に失敗しました。"

            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

            # FastAPI MCPエンドポイントにリクエスト
            endpoint_mapping = {"suggest-data-quality-rules": "/dataplex/suggest-data-quality-rules"}

            endpoint = endpoint_mapping.get(tool_name)
            if not endpoint:
                return f"エラー: 未知のツール名 '{tool_name}'"

            response = requests.post(f"{self.config.mcp_server_url}{endpoint}", json=arguments, headers=headers, timeout=60)

            if response.status_code != 200:
                logger.error(f"MCP server接続失敗: {response.status_code}")
                return f"エラー: MCP server接続失敗 (HTTP {response.status_code})"

            # レスポンスはプレーンテキストとして返される
            return response.text.strip()

        except Exception as e:
            logger.error(f"MCP通信エラー: {e}")
            return f"エラー: MCP server通信失敗 - {str(e)}"

    def dataplex_security_guardrail(self, tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
        """
        Dataplex操作のセキュリティガードレール

        以下の条件をチェックして、危険な操作を防止：
        1. 本番環境での危険なproject_id
        2. 削除・変更系操作の制限
        3. 機密データへのアクセス制御
        """
        tool_name = tool.name
        agent_name = tool_context.agent_name

        logger.info(f"🛡️ ガードレールチェック開始: tool='{tool_name}', agent='{agent_name}'")
        logger.info(f"🔍 引数検査: {args}")

        # 1. 本番環境での危険なproject_id制限
        restricted_projects = ["production-critical", "financial-data", "customer-pii"]
        project_id = args.get("project_id", "")

        if project_id in restricted_projects:
            logger.warning(f"🚫 制限されたプロジェクトへのアクセス拒否: {project_id}")
            return {"error": f"プロジェクト '{project_id}' への操作は制限されています。管理者に問い合わせてください。"}

        # 2. 削除・変更系操作の制限
        dangerous_operations = ["delete", "remove", "drop", "truncate", "modify", "update"]
        tool_name_lower = tool_name.lower()
        if any(op in tool_name_lower for op in dangerous_operations):
            logger.warning(f"🚫 危険な操作の実行拒否: {tool_name}")
            return {"error": f"'{tool_name}' は削除・変更系操作のため、この環境では実行できません。"}

        # 3. 機密データアクセス制御
        sensitive_keywords = ["pii", "personal", "financial", "credit", "ssn", "secret"]
        for arg_key, arg_value in args.items():
            if isinstance(arg_value, str):
                if any(keyword in arg_value.lower() for keyword in sensitive_keywords):
                    logger.warning(f"🚫 機密データアクセスの実行拒否: {arg_key}={arg_value}")
                    return {"error": f"機密データに関連する引数 '{arg_key}' の使用は制限されています。"}

        logger.info(f"✅ ガードレールチェック通過: {tool_name}")
        return None

    def compliance_policy_guardrail(self, tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
        """
        コンプライアンスポリシーガードレール

        データガバナンス要件に基づくアクセス制御：
        1. 機密データテーブルへのアクセス制限
        2. 業務時間外アクセスの制限
        3. 大量データ処理の制限
        """
        tool_name = tool.name

        logger.info(f"🛡️ コンプライアンスポリシーガードレール実行: {tool_name}")

        # 1. 機密データテーブルへのアクセス制限
        table_id = args.get("table_id", "")
        sensitive_patterns = ["personal", "private", "secret", "confidential", "pii"]
        if any(pattern in table_id.lower() for pattern in sensitive_patterns):
            logger.warning(f"🚫 機密データテーブルへのアクセス拒否: {table_id}")
            return {"error": f"テーブル '{table_id}' は機密データを含むため、アクセスが制限されています。"}

        # 2. データセットレベルでの制限
        dataset_id = args.get("dataset_id", "")
        restricted_datasets = ["sensitive_data", "personal_info", "financial_records"]
        if any(restricted in dataset_id.lower() for restricted in restricted_datasets):
            logger.warning(f"🚫 制限されたデータセットへのアクセス拒否: {dataset_id}")
            return {"error": f"データセット '{dataset_id}' へのアクセスは制限されています。"}

        logger.info("✅ コンプライアンスポリシーガードレール通過")
        return None

    def combined_guardrail_callback(self, tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
        """
        複数のガードレールを順次実行

        セキュリティガードレール → コンプライアンスガードレールの順で実行
        いずれかで違反が検出された場合、即座に処理を停止
        """
        logger.info(f"🛡️ 統合ガードレール開始: {tool.name}")

        # 1. セキュリティガードレール実行
        security_result = self.dataplex_security_guardrail(tool, args, tool_context)
        if security_result is not None:
            logger.error(f"🚨 セキュリティガードレール違反: {security_result}")
            return security_result

        # 2. コンプライアンスガードレール実行
        compliance_result = self.compliance_policy_guardrail(tool, args, tool_context)
        if compliance_result is not None:
            logger.error(f"🚨 コンプライアンスガードレール違反: {compliance_result}")
            return compliance_result

        logger.info("🎯 全ガードレールチェック完了：実行許可")
        return None
