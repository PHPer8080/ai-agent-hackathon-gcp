"""
Dataplex Data Quality Rules専用サービス

BigQuery統計情報とDataplex APIを活用した詳細な品質ルール提案に特化
"""

import json
import logging
from datetime import datetime

from google.cloud import dataplex_v1

logger = logging.getLogger(__name__)


class DataplexService:
    """Dataplex Data Quality Rules専用サービス"""

    def __init__(self):
        """Dataplexサービス初期化"""
        logger.info("🚀 DataplexService 初期化開始")

        # Dataplex Data Scan クライアント
        self.data_scan_client = dataplex_v1.DataScanServiceClient()

        logger.info("✅ DataplexService 初期化完了")

    async def cleanup(self):
        """リソースのクリーンアップ"""
        logger.info("🔄 DataplexService リソースクリーンアップ")

        # クライアントのクリーンアップ
        if hasattr(self, "data_scan_client"):
            self.data_scan_client.transport.close()

    async def suggest_data_quality_rules(self, project_id: str, dataset_id: str, table_id: str, bigquery_statistics: dict = None) -> str:
        """
        BigQuery統計情報とDataplex APIを活用した詳細なデータ品質ルール提案

        Args:
            project_id: プロジェクトID
            dataset_id: データセットID
            table_id: テーブルID
            bigquery_statistics: BigQuery統計情報（オプション）

        Returns:
            str: 提案されたルール（JSON形式）
        """
        try:
            logger.info(f"🔍 データ品質ルール提案開始: {project_id}.{dataset_id}.{table_id}")

            # 既存のDataplexスキャン情報を取得
            existing_scans = await self._get_existing_scans(project_id, dataset_id, table_id)

            # BigQuery統計情報の解析
            statistics_analysis = self._analyze_bigquery_statistics(bigquery_statistics) if bigquery_statistics else {}

            # 基本的な品質ルール提案
            suggested_rules = []

            # 統計情報がある場合の詳細提案
            if statistics_analysis:
                suggested_rules.extend(self._generate_statistical_rules(statistics_analysis))

            # 一般的な品質ルール提案
            suggested_rules.extend(self._generate_general_rules(dataset_id, table_id))

            # 結果の構築
            result = {
                "target_table": {"project_id": project_id, "dataset_id": dataset_id, "table_id": table_id, "full_name": f"{project_id}.{dataset_id}.{table_id}"},
                "existing_scans": existing_scans,
                "statistics_analysis": statistics_analysis,
                "suggested_rules": suggested_rules,
                "implementation_guidance": {
                    "recommended_approach": "Cloud Console または gcloud CLI",
                    "steps": ["1. 提案されたルールを確認・調整", "2. Cloud Consoleでデータスキャンを作成", "3. 定期実行スケジュールを設定", "4. 品質ルールを適用", "5. 動作確認とモニタリング設定"],
                },
                "generated_at": datetime.now().isoformat(),
            }

            logger.info(f"✅ データ品質ルール提案完了: {len(suggested_rules)}個のルール")
            return json.dumps(result, indent=2, ensure_ascii=False)

        except Exception as e:
            error_message = f"データ品質ルール提案エラー: {str(e)}"
            logger.error(f"❌ {error_message}")
            return json.dumps({"error": error_message, "project_id": project_id, "dataset_id": dataset_id, "table_id": table_id})

    async def _get_existing_scans(self, project_id: str, dataset_id: str, table_id: str) -> list:
        """既存のDataplexスキャン情報を取得"""
        try:
            parent = f"projects/{project_id}/locations/asia-northeast1"
            request = dataplex_v1.ListDataScansRequest(parent=parent)

            existing_scans = []
            page_result = self.data_scan_client.list_data_scans(request=request)

            for scan in page_result:
                # BigQueryテーブルに関連するスキャンをフィルタ
                if scan.data and scan.data.entity and f"{dataset_id}/{table_id}" in scan.data.entity:
                    existing_scans.append(
                        {
                            "name": scan.name,
                            "display_name": scan.display_name,
                            "state": scan.state.name if scan.state else "UNKNOWN",
                            "type": "DATA_QUALITY" if scan.data_quality_spec else "DATA_PROFILE",
                        }
                    )

            return existing_scans

        except Exception as e:
            logger.warning(f"既存スキャン取得エラー: {e}")
            return []

    def _analyze_bigquery_statistics(self, statistics: dict) -> dict:
        """BigQuery統計情報の解析"""
        analysis = {"total_columns": 0, "nullable_columns": [], "numeric_columns": [], "string_columns": [], "timestamp_columns": [], "recommendations": []}

        if not statistics:
            return analysis

        # column_statisticsの解析
        column_stats = statistics.get("column_statistics", [])
        analysis["total_columns"] = len(column_stats)

        for col_stat in column_stats:
            column_name = col_stat.get("column_name", "")
            data_type = col_stat.get("data_type", "")
            null_count = col_stat.get("null_count", 0)

            # データタイプ別分類
            if "INT" in data_type or "FLOAT" in data_type or "NUMERIC" in data_type:
                analysis["numeric_columns"].append(column_name)
            elif "STRING" in data_type:
                analysis["string_columns"].append(column_name)
            elif "TIMESTAMP" in data_type or "DATE" in data_type:
                analysis["timestamp_columns"].append(column_name)

            # NULL値チェック
            if null_count > 0:
                analysis["nullable_columns"].append(column_name)

        return analysis

    def _generate_statistical_rules(self, analysis: dict) -> list:
        """統計情報に基づく詳細ルール生成"""
        rules = []

        # 数値カラムの範囲チェック
        for column in analysis.get("numeric_columns", []):
            rules.append({"rule_type": "RANGE_CHECK", "column": column, "priority": "MEDIUM", "description": f"数値範囲チェック: {column}", "rationale": "統計情報に基づく数値範囲の妥当性検証"})

        # 文字列カラムの長さチェック
        for column in analysis.get("string_columns", []):
            rules.append({"rule_type": "STRING_LENGTH_CHECK", "column": column, "priority": "LOW", "description": f"文字列長チェック: {column}", "rationale": "文字列の長さ制限による品質保証"})

        # タイムスタンプカラムの妥当性チェック
        for column in analysis.get("timestamp_columns", []):
            rules.append({"rule_type": "TIMESTAMP_VALIDITY", "column": column, "priority": "HIGH", "description": f"タイムスタンプ妥当性チェック: {column}", "rationale": "時系列データの整合性保証"})

        return rules

    def _generate_general_rules(self, dataset_id: str, table_id: str) -> list:
        """一般的な品質ルール生成"""
        rules = [
            {"rule_type": "NOT_NULL", "column": "id", "priority": "HIGH", "description": "主キーのNULL値チェック", "rationale": "データの一意性保証のため"},
            {"rule_type": "UNIQUENESS", "column": "id", "priority": "HIGH", "description": "主キーの一意性チェック", "rationale": "重複データの検出・防止"},
            {"rule_type": "ROW_COUNT", "priority": "MEDIUM", "description": "テーブル行数チェック", "rationale": "データ欠損の早期検出"},
        ]

        # テーブル名に基づく特定ルール
        if "customer" in table_id.lower():
            rules.append({"rule_type": "EMAIL_FORMAT", "column": "email", "priority": "HIGH", "description": "メールアドレス形式チェック", "rationale": "顧客データの品質保証"})

        return rules
