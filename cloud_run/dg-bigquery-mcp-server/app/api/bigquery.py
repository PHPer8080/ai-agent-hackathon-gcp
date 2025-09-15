"""
BigQuery API エンドポイント
"""

import json
import logging

from fastapi import APIRouter

from app.core.config import get_settings
from app.services.bigquery_service import BigQueryService

logger = logging.getLogger(__name__)
settings = get_settings()

# BigQueryサービスインスタンス
bigquery_service = BigQueryService()

# APIルーター
router = APIRouter(prefix="/bigquery", tags=["BigQuery"])


@router.post("/datasets", operation_id="get_bigquery_datasets")
async def get_bigquery_datasets(request: dict) -> str:
    """BigQueryデータセット一覧取得"""
    project_id = request.get("project_id") or settings.project_id

    result = await bigquery_service.get_datasets(project_id)
    logger.info("✅ ツール実行完了: get_bigquery_datasets")
    return result


@router.post("/tables/missing-description", operation_id="find_tables_missing_description")
async def find_tables_missing_description(request: dict) -> str:
    """説明が不足しているテーブルを検出"""
    project_id = request.get("project_id") or settings.project_id
    dataset_id = request.get("dataset_id")

    result = await bigquery_service.find_tables_missing_description(project_id, dataset_id)
    logger.info("✅ ツール実行完了: find_tables_missing_description")
    return result


@router.post("/tables/missing-logical-name", operation_id="find_tables_missing_logical_name")
async def find_tables_missing_logical_name(request: dict) -> str:
    """論理名（ラベル）が不足しているテーブルを検出"""
    project_id = request.get("project_id") or settings.project_id
    dataset_id = request.get("dataset_id")

    result = await bigquery_service.find_tables_missing_logical_name(project_id, dataset_id)
    logger.info("✅ ツール実行完了: find_tables_missing_logical_name")
    return result


@router.post("/table/suggest-logical-name", operation_id="suggest_logical_name")
async def suggest_logical_name(request: dict) -> str:
    """テーブル名とスキーマから論理名を提案"""
    project_id = request.get("project_id") or settings.project_id
    dataset_id = request.get("dataset_id")
    table_name = request.get("table_name")

    if not dataset_id or not table_name:
        return json.dumps({"error": "dataset_idとtable_nameが必要です"})

    result = await bigquery_service.suggest_logical_name(project_id, dataset_id, table_name)
    logger.info("✅ ツール実行完了: suggest_logical_name")
    return result


@router.post("/table/suggest-description", operation_id="suggest_description")
async def suggest_description(request: dict) -> str:
    """テーブル名とスキーマから説明を提案"""
    project_id = request.get("project_id") or settings.project_id
    dataset_id = request.get("dataset_id")
    table_name = request.get("table_name")

    if not dataset_id or not table_name:
        return json.dumps({"error": "dataset_idとtable_nameが必要です"})

    result = await bigquery_service.suggest_description(project_id, dataset_id, table_name)
    logger.info("✅ ツール実行完了: suggest_description")
    return result


@router.post("/table/check-column-descriptions", operation_id="check_column_descriptions")
async def check_column_descriptions(request: dict) -> str:
    """特定テーブルのカラム説明（論理名）を確認"""
    project_id = request.get("project_id") or settings.project_id
    dataset_id = request.get("dataset_id")
    table_name = request.get("table_name")

    if not dataset_id or not table_name:
        return json.dumps({"error": "dataset_idとtable_nameが必要です"})

    result = await bigquery_service.check_column_descriptions(project_id, dataset_id, table_name)
    logger.info("✅ ツール実行完了: check_column_descriptions")
    return result


@router.post("/lineage", operation_id="get_table_lineage")
async def get_table_lineage(request: dict) -> str:
    """BigQueryテーブルの依存関係（リネージ）を取得"""
    project_id = request.get("project_id") or settings.project_id
    dataset_id = request.get("dataset_id")
    table_id = request.get("table_id")

    if not dataset_id or not table_id:
        return json.dumps({"error": "dataset_idとtable_idが必要です"})

    result = await bigquery_service.get_table_lineage(project_id, dataset_id, table_id)
    logger.info("✅ ツール実行完了: get_table_lineage")
    return result


@router.post("/governance-score", operation_id="calculate_governance_score")
async def calculate_governance_score(request: dict) -> str:
    """BigQueryテーブルのガバナンススコアを計算"""
    project_id = request.get("project_id") or settings.project_id
    dataset_id = request.get("dataset_id")
    table_id = request.get("table_id")

    result = await bigquery_service.calculate_governance_score(project_id, dataset_id, table_id)
    logger.info("✅ ツール実行完了: calculate_governance_score")
    return json.dumps(result, ensure_ascii=False, indent=2)


@router.post("/table-statistics", operation_id="get_table_statistics")
async def get_table_statistics(request: dict) -> str:
    """BigQueryテーブルの詳細統計情報を取得（データ品質分析用）"""
    project_id = request.get("project_id") or settings.project_id
    dataset_id = request.get("dataset_id")
    table_id = request.get("table_id")

    result = await bigquery_service.get_table_statistics(project_id, dataset_id, table_id)
    logger.info("✅ ツール実行完了: get_table_statistics")
    return json.dumps(result, ensure_ascii=False, indent=2)
