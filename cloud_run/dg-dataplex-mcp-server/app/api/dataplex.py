"""
Dataplex API エンドポイント
"""

import json
import logging

from fastapi import APIRouter

from app.core.config import get_settings
from app.services.dataplex_service import DataplexService

logger = logging.getLogger(__name__)
settings = get_settings()

# Dataplexサービスインスタンス
dataplex_service = DataplexService()

# APIルーター
router = APIRouter(prefix="/dataplex", tags=["Dataplex"])


@router.post("/suggest-data-quality-rules", operation_id="suggest_data_quality_rules")
async def suggest_data_quality_rules(request: dict) -> str:
    """BigQuery統計情報に基づくデータ品質ルールの提案"""
    project_id = request.get("project_id") or settings.project_id
    dataset_id = request.get("dataset_id", "")
    table_id = request.get("table_id", "")
    bigquery_statistics = request.get("bigquery_statistics")  # BigQuery統計情報を受け取る

    if not dataset_id or not table_id:
        return json.dumps({"error": "dataset_idとtable_idが必要です", "example": "dataset_id='tt_us', table_id='product_catalog'", "description": "指定されたテーブルのデータ品質ルールを提案します"})

    result = await dataplex_service.suggest_data_quality_rules(project_id, dataset_id, table_id, bigquery_statistics)
    logger.info("✅ ツール実行完了: suggest_data_quality_rules")
    return result
