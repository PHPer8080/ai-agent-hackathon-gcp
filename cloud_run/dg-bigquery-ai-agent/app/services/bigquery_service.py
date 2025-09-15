"""
BigQueryサービス

BigQuery関連のツール機能とガードレール機能
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


class BigQueryService:
    """BigQueryサービス"""

    def __init__(self):
        self.config = AgentConfig()
        self.config.load_environment_variables()
        self.auth_service = AuthService()

    # BigQuery API ツール関数群
    def get_bigquery_datasets(self, project_id: str = "your-project-id") -> str:  # FIXME: プロジェクトIDを適宜変更
        """BigQueryデータセット一覧を取得"""
        return self.call_mcp_server("get-bigquery-datasets", {"project_id": project_id})

    def get_table_lineage(self, project_id: str = "your-project-id", dataset_id: str = "", table_id: str = "") -> str:  # FIXME: プロジェクトIDを適宜変更
        """BigQueryテーブルの依存関係（リネージ）を取得"""
        return self.call_mcp_server("get-table-lineage", {"project_id": project_id, "dataset_id": dataset_id, "table_id": table_id})

    def find_tables_missing_description(self, project_id: str = "your-project-id", dataset_id: str = "") -> str:  # FIXME: プロジェクトIDを適宜変更
        """説明（description）が不足しているテーブルを検出"""
        return self.call_mcp_server("find-tables-missing-description", {"project_id": project_id, "dataset_id": dataset_id})

    def find_tables_missing_logical_name(self, project_id: str = "your-project-id", dataset_id: str = "") -> str:  # FIXME: プロジェクトIDを適宜変更
        """論理名（ラベル）が不足しているテーブルを検出"""
        return self.call_mcp_server("find-tables-missing-logical-name", {"project_id": project_id, "dataset_id": dataset_id})

    def suggest_logical_name(self, project_id: str = "your-project-id", dataset_id: str = "", table_name: str = "") -> str:  # FIXME: プロジェクトIDを適宜変更
        """テーブル名とスキーマから論理名を提案"""
        return self.call_mcp_server("suggest-logical-name", {"project_id": project_id, "dataset_id": dataset_id, "table_name": table_name})

    def suggest_description(self, project_id: str = "your-project-id", dataset_id: str = "", table_name: str = "") -> str:  # FIXME: プロジェクトIDを適宜変更
        """テーブル名とスキーマから説明を提案"""
        return self.call_mcp_server("suggest-description", {"project_id": project_id, "dataset_id": dataset_id, "table_name": table_name})

    def check_column_descriptions(self, project_id: str = "your-project-id", dataset_id: str = "", table_name: str = "") -> str:  # FIXME: プロジェクトIDを適宜変更
        """特定テーブルのカラム説明（論理名）を確認"""
        return self.call_mcp_server("check-column-descriptions", {"project_id": project_id, "dataset_id": dataset_id, "table_name": table_name})

    def calculate_governance_score(self, project_id: str, dataset_id: str, table_id: str) -> str:
        """単一テーブルのガバナンススコアを計算（説明・論理名・カラム説明・ラベル等を総合評価）"""
        return self.call_mcp_server("calculate_governance_score", {"project_id": project_id, "dataset_id": dataset_id, "table_id": table_id})

    def get_table_statistics(self, project_id: str, dataset_id: str, table_id: str) -> str:
        """テーブルのカラム統計情報を取得（データ品質分析用）- NULL率、データ型、値の分布等を分析"""
        return self.call_mcp_server("get_table_statistics", {"project_id": project_id, "dataset_id": dataset_id, "table_id": table_id})

    def call_mcp_server(self, tool_name: str, arguments: dict) -> str:
        """MCPサーバーへリクエスト送信"""
        if not self.config or not self.config.mcp_server_url:
            return "エラー: MCP サーバー接続が設定されていません。"

        try:
            token = self.auth_service.get_identity_token(self.config.mcp_server_url)
            if not token:
                return "エラー: 認証トークンの取得に失敗しました。"

            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

            # FastAPI MCPエンドポイントにリクエスト
            endpoint_mapping = {
                "get-bigquery-datasets": "/bigquery/datasets",
                "get-table-lineage": "/bigquery/lineage",
                "find-tables-missing-description": "/bigquery/tables/missing-description",
                "find-tables-missing-logical-name": "/bigquery/tables/missing-logical-name",
                "suggest-logical-name": "/bigquery/table/suggest-logical-name",
                "suggest-description": "/bigquery/table/suggest-description",
                "check-column-descriptions": "/bigquery/table/check-column-descriptions",
                "calculate_governance_score": "/bigquery/governance-score",
                "get_table_statistics": "/bigquery/table-statistics",
            }

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

    # ガードレール関数群
    def bigquery_security_guardrail(self, tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
        """
        BigQuery操作のセキュリティガードレール

        以下の条件をチェックして、危険な操作を防止：
        1. 本番環境での危険なproject_id
        2. 削除・変更系操作の制限
        3. 機密データへのアクセス制御
        4. 危険なクエリパターンの検出
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

        # 4. 危険なクエリパターンの検出
        query = args.get("query", "")
        if query:
            dangerous_query_patterns = ["drop table", "delete from", "truncate table", "alter table", "create table"]
            query_lower = query.lower()
            if any(pattern in query_lower for pattern in dangerous_query_patterns):
                logger.warning(f"🚫 危険なクエリパターンの実行拒否: {query}")
                return {"error": "危険なクエリパターンが検出されました。読み取り専用のクエリのみ実行可能です。"}

        logger.info(f"✅ ガードレールチェック通過: {tool_name}")
        return None

    def compliance_policy_guardrail(self, tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
        """
        コンプライアンス・ポリシーガードレール

        監査ログ記録を実行：
        1. 全ツール実行の詳細ログ記録
        """
        tool_name = tool.name

        # 監査ログ記録
        logger.info(f"📝 監査ログ: user={tool_context.agent_name}, tool={tool_name}, args={args}")
        return None

    def combined_guardrail_callback(self, tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
        """複数のガードレールを順次実行"""
        # 🛡️ ガードレール実行順序定義
        guardrail_checks = [
            self.bigquery_security_guardrail,
            self.compliance_policy_guardrail,
        ]

        for guardrail_func in guardrail_checks:
            if result := guardrail_func(tool, args, tool_context):
                return result

        # 全てのガードレール通過
        logger.info(f"🎉 全ガードレール通過: {tool.name}")
        return None
