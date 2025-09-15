"""
BigQuery サービス

BigQueryデータガバナンス機能を提供
"""

import json
import logging
from datetime import datetime

from google.cloud import bigquery

logger = logging.getLogger(__name__)


class BigQueryService:
    """BigQuery サービスクラス"""

    def __init__(self):
        """初期化"""
        logger.info("🚀 BigQueryService初期化")

    async def __aenter__(self):
        """非同期コンテキストマネージャー開始"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """非同期コンテキストマネージャー終了"""
        await self.close()

    async def close(self):
        """リソースのクリーンアップ"""
        logger.info("🔄 BigQueryService リソースクリーンアップ")

    async def get_datasets(self, project_id: str) -> str:
        """
        BigQueryデータセット一覧を取得

        Args:
            project_id: プロジェクトID

        Returns:
            str: データセット一覧（JSON形式）
        """
        try:
            logger.info(f"🔄 BigQueryデータセット一覧取得開始: {project_id}")

            # BigQuery クライアント初期化
            client = bigquery.Client(project=project_id)

            # データセット一覧を取得
            datasets = []
            for dataset in client.list_datasets():
                dataset_ref = client.get_dataset(dataset.dataset_id)

                # テーブル数を取得
                table_count = len(list(client.list_tables(dataset_ref)))

                dataset_info = {
                    "dataset_id": dataset.dataset_id,
                    "location": dataset_ref.location,
                    "creation_time": dataset_ref.created.isoformat()
                    if dataset_ref.created
                    else None,
                    "last_modified_time": dataset_ref.modified.isoformat()
                    if dataset_ref.modified
                    else None,
                    "description": dataset_ref.description or "なし",
                    "description_status": "あり"
                    if dataset_ref.description and dataset_ref.description.strip()
                    else "なし",
                    "table_count": table_count,
                }
                datasets.append(dataset_info)

            result = {
                "project_id": project_id,
                "datasets": datasets,
                "total_datasets": len(datasets),
            }

            logger.info(f"✅ BigQueryデータセット一覧取得完了: {len(datasets)}個")
            return json.dumps(result, indent=2, ensure_ascii=False)

        except Exception as e:
            error_message = f"BigQueryデータセット一覧取得エラー: {str(e)}"
            logger.error(f"❌ {error_message}")
            return json.dumps({"error": error_message, "project_id": project_id})

    async def find_tables_missing_description(
        self, project_id: str, dataset_id: str = None
    ) -> str:
        """
        説明が不足しているテーブルを検出

        Args:
            project_id: プロジェクトID
            dataset_id: データセットID（オプション）

        Returns:
            str: 説明不足テーブル一覧（JSON形式）
        """
        try:
            logger.info(f"🔄 説明不足テーブル検出開始: {project_id}")

            # BigQuery クライアント初期化
            client = bigquery.Client(project=project_id)

            missing_description_tables = []

            # データセット一覧を取得
            datasets_to_check = []
            if dataset_id:
                datasets_to_check = [client.get_dataset(dataset_id)]
            else:
                datasets_to_check = list(client.list_datasets())

            for dataset in datasets_to_check:
                dataset_ref = client.get_dataset(dataset.dataset_id)

                # テーブル一覧を取得
                for table_ref in client.list_tables(dataset_ref):
                    table = client.get_table(table_ref)

                    # 説明が不足している場合
                    if not table.description or not table.description.strip():
                        issue_type = (
                            "description が NULL"
                            if table.description is None
                            else "description が空文字"
                        )

                        # 優先度を判定
                        priority = "低優先度"
                        if table.num_bytes and table.num_bytes > 1000000000:  # 1GB以上
                            priority = "高優先度"
                        elif table.num_rows and table.num_rows > 1000000:  # 100万行以上
                            priority = "高優先度"
                        elif table.table_id and not any(
                            x in table.table_id.lower() for x in ["temp", "tmp", "test"]
                        ):
                            priority = "中優先度"

                        table_info = {
                            "project_id": project_id,
                            "dataset_id": dataset.dataset_id,
                            "table_name": table.table_id,
                            "table_type": str(table.table_type),
                            "creation_time": table.created.isoformat()
                            if table.created
                            else None,
                            "last_modified_time": table.modified.isoformat()
                            if table.modified
                            else None,
                            "column_count": len(table.schema),
                            "row_count": table.num_rows or 0,
                            "size_mb": round((table.num_bytes or 0) / 1024 / 1024, 2),
                            "issue_type": issue_type,
                            "priority": priority,
                        }
                        missing_description_tables.append(table_info)

            # 優先度順にソート
            priority_order = {"高優先度": 1, "中優先度": 2, "低優先度": 3}
            missing_description_tables.sort(
                key=lambda x: (
                    priority_order.get(x["priority"], 4),
                    -x["size_mb"],
                    x["table_name"],
                )
            )

            result = {
                "project_id": project_id,
                "dataset_id": dataset_id,
                "tables_missing_description": missing_description_tables,
                "total_tables": len(missing_description_tables),
                "summary": {
                    "high_priority": len(
                        [
                            t
                            for t in missing_description_tables
                            if t["priority"] == "高優先度"
                        ]
                    ),
                    "medium_priority": len(
                        [
                            t
                            for t in missing_description_tables
                            if t["priority"] == "中優先度"
                        ]
                    ),
                    "low_priority": len(
                        [
                            t
                            for t in missing_description_tables
                            if t["priority"] == "低優先度"
                        ]
                    ),
                },
            }

            logger.info(
                f"✅ 説明不足テーブル検出完了: {len(missing_description_tables)}個"
            )
            return json.dumps(result, indent=2, ensure_ascii=False)

        except Exception as e:
            error_message = f"説明不足テーブル検出エラー: {str(e)}"
            logger.error(f"❌ {error_message}")
            return json.dumps(
                {
                    "error": error_message,
                    "project_id": project_id,
                    "dataset_id": dataset_id,
                }
            )

    async def find_tables_missing_logical_name(
        self, project_id: str, dataset_id: str = None
    ) -> str:
        """
        論理名（ラベル）が不足しているテーブルを検出

        Args:
            project_id: プロジェクトID
            dataset_id: データセットID（オプション）

        Returns:
            str: 論理名不足テーブル一覧（JSON形式）
        """
        try:
            logger.info(f"🔄 論理名不足テーブル検出開始: {project_id}")

            # BigQuery クライアント初期化
            client = bigquery.Client(project=project_id)

            missing_logical_name_tables = []

            # データセット一覧を取得
            datasets_to_check = []
            if dataset_id:
                datasets_to_check = [client.get_dataset(dataset_id)]
            else:
                datasets_to_check = list(client.list_datasets())

            for dataset in datasets_to_check:
                dataset_ref = client.get_dataset(dataset.dataset_id)

                # テーブル一覧を取得
                for table_ref in client.list_tables(dataset_ref):
                    table = client.get_table(table_ref)

                    # ラベル（論理名）が不足している場合
                    if not table.labels:
                        # 優先度を判定
                        priority = "低優先度"
                        if table.num_bytes and table.num_bytes > 1000000000:  # 1GB以上
                            priority = "高優先度"
                        elif table.num_rows and table.num_rows > 1000000:  # 100万行以上
                            priority = "高優先度"
                        elif table.table_id and not any(
                            x in table.table_id.lower() for x in ["temp", "tmp", "test"]
                        ):
                            priority = "中優先度"

                        table_info = {
                            "project_id": project_id,
                            "dataset_id": dataset.dataset_id,
                            "table_name": table.table_id,
                            "table_type": str(table.table_type),
                            "creation_time": table.created.isoformat()
                            if table.created
                            else None,
                            "last_modified_time": table.modified.isoformat()
                            if table.modified
                            else None,
                            "column_count": len(table.schema),
                            "row_count": table.num_rows or 0,
                            "size_mb": round((table.num_bytes or 0) / 1024 / 1024, 2),
                            "issue_type": "論理名（ラベル）なし",
                            "priority": priority,
                        }
                        missing_logical_name_tables.append(table_info)

            # 優先度順にソート
            priority_order = {"高優先度": 1, "中優先度": 2, "低優先度": 3}
            missing_logical_name_tables.sort(
                key=lambda x: (
                    priority_order.get(x["priority"], 4),
                    -x["size_mb"],
                    x["table_name"],
                )
            )

            result = {
                "project_id": project_id,
                "dataset_id": dataset_id,
                "tables_missing_logical_name": missing_logical_name_tables,
                "total_tables": len(missing_logical_name_tables),
                "summary": {
                    "high_priority": len(
                        [
                            t
                            for t in missing_logical_name_tables
                            if t["priority"] == "高優先度"
                        ]
                    ),
                    "medium_priority": len(
                        [
                            t
                            for t in missing_logical_name_tables
                            if t["priority"] == "中優先度"
                        ]
                    ),
                    "low_priority": len(
                        [
                            t
                            for t in missing_logical_name_tables
                            if t["priority"] == "低優先度"
                        ]
                    ),
                },
            }

            logger.info(
                f"✅ 論理名不足テーブル検出完了: {len(missing_logical_name_tables)}個"
            )
            return json.dumps(result, indent=2, ensure_ascii=False)

        except Exception as e:
            error_message = f"論理名不足テーブル検出エラー: {str(e)}"
            logger.error(f"❌ {error_message}")
            return json.dumps(
                {
                    "error": error_message,
                    "project_id": project_id,
                    "dataset_id": dataset_id,
                }
            )

    async def suggest_logical_name(
        self, project_id: str, dataset_id: str, table_name: str
    ) -> str:
        """
        テーブル名とスキーマから論理名を提案

        Args:
            project_id: プロジェクトID
            dataset_id: データセットID
            table_name: テーブル名

        Returns:
            str: 論理名提案（JSON形式）
        """
        try:
            logger.info(f"🔄 論理名提案開始: {dataset_id}.{table_name}")

            # BigQuery クライアント初期化
            client = bigquery.Client(project=project_id)

            # テーブル取得
            table_ref = client.dataset(dataset_id).table(table_name)
            table = client.get_table(table_ref)

            # サンプルデータを取得（最大5行）
            sample_data = []
            try:
                query = f"""
                SELECT *
                FROM `{project_id}.{dataset_id}.{table_name}`
                LIMIT 5
                """
                query_job = client.query(query)
                results = query_job.result()

                for row in results:
                    row_dict = {}
                    for field in table.schema:
                        value = row.get(field.name)
                        # 値を文字列に変換（長すぎる場合は切り詰め）
                        if value is not None:
                            str_value = str(value)
                            if len(str_value) > 100:
                                str_value = str_value[:100] + "..."
                            row_dict[field.name] = str_value
                        else:
                            row_dict[field.name] = None
                    sample_data.append(row_dict)

                logger.info(f"📊 サンプルデータ取得完了: {len(sample_data)}行")
            except Exception as e:
                logger.warning(f"⚠️ サンプルデータ取得失敗: {str(e)}")
                sample_data = []

            # テーブル名から論理名を推測
            suggestions = []

            # パターン1: テーブル名ベース
            if "embedding" in table_name.lower():
                suggestions.append(
                    {
                        "key": "data_type",
                        "value": "embedding",
                        "reason": "テーブル名に'embedding'が含まれる",
                    }
                )
            elif "rag" in table_name.lower():
                suggestions.append(
                    {
                        "key": "data_type",
                        "value": "rag",
                        "reason": "テーブル名に'rag'が含まれる",
                    }
                )
            elif "master" in table_name.lower():
                suggestions.append(
                    {
                        "key": "table_type",
                        "value": "master",
                        "reason": "テーブル名に'master'が含まれる",
                    }
                )

            # パターン2: データセット名ベース
            if dataset_id == "tt_us":
                suggestions.append(
                    {
                        "key": "location",
                        "value": "us",
                        "reason": "USロケーションのデータセット",
                    }
                )

            # パターン3: 汎用ラベル
            suggestions.append(
                {"key": "environment", "value": "stg", "reason": "ステージング環境"}
            )
            suggestions.append(
                {
                    "key": "managed_by",
                    "value": "data_team",
                    "reason": "データチーム管理",
                }
            )

            result = {
                "project_id": project_id,
                "dataset_id": dataset_id,
                "table_name": table_name,
                "current_labels": dict(table.labels) if table.labels else {},
                "suggested_labels": suggestions,
                "table_info": {
                    "table_type": str(table.table_type),
                    "column_count": len(table.schema),
                    "size_mb": round((table.num_bytes or 0) / 1024 / 1024, 2),
                },
                "sample_data": sample_data,
                "sample_data_count": len(sample_data),
            }

            logger.info(f"✅ 論理名提案完了: {dataset_id}.{table_name}")
            return json.dumps(result, indent=2, ensure_ascii=False)

        except Exception as e:
            error_message = f"論理名提案エラー: {str(e)}"
            logger.error(f"❌ {error_message}")
            return json.dumps(
                {
                    "error": error_message,
                    "project_id": project_id,
                    "dataset_id": dataset_id,
                    "table_name": table_name,
                }
            )

    async def suggest_description(
        self, project_id: str, dataset_id: str, table_name: str
    ) -> str:
        """
        テーブル名とスキーマから説明を提案

        Args:
            project_id: プロジェクトID
            dataset_id: データセットID
            table_name: テーブル名

        Returns:
            str: 説明提案（JSON形式）
        """
        try:
            logger.info(f"🔄 説明提案開始: {dataset_id}.{table_name}")

            # BigQuery クライアント初期化
            client = bigquery.Client(project=project_id)

            # テーブル取得
            table_ref = client.dataset(dataset_id).table(table_name)
            table = client.get_table(table_ref)

            # サンプルデータを取得（最大5行）
            sample_data = []
            try:
                query = f"""
                SELECT *
                FROM `{project_id}.{dataset_id}.{table_name}`
                LIMIT 5
                """
                query_job = client.query(query)
                results = query_job.result()

                for row in results:
                    row_dict = {}
                    for field in table.schema:
                        value = row.get(field.name)
                        # 値を文字列に変換（長すぎる場合は切り詰め）
                        if value is not None:
                            str_value = str(value)
                            if len(str_value) > 100:
                                str_value = str_value[:100] + "..."
                            row_dict[field.name] = str_value
                        else:
                            row_dict[field.name] = None
                    sample_data.append(row_dict)

                logger.info(f"📊 サンプルデータ取得完了: {len(sample_data)}行")
            except Exception as e:
                logger.warning(f"⚠️ サンプルデータ取得失敗: {str(e)}")
                sample_data = []

            # テーブル名とスキーマから説明を推測
            suggestions = []

            # パターン1: テーブル名ベース
            if "embedding" in table_name.lower():
                if "wagahai" in table_name.lower():
                    suggestions.append(
                        "「吾輩は猫である」テキストのベクトル埋め込みデータ"
                    )
                else:
                    suggestions.append(
                        "テキストのベクトル埋め込みデータを格納するテーブル"
                    )
            elif "rag" in table_name.lower():
                if "master" in table_name.lower():
                    suggestions.append(
                        "RAG（Retrieval-Augmented Generation）システムのマスターデータ"
                    )
                elif "wagahai" in table_name.lower():
                    suggestions.append("「吾輩は猫である」のRAG処理結果データ")
                else:
                    suggestions.append(
                        "RAG（Retrieval-Augmented Generation）システムのデータ"
                    )

            # パターン2: スキーマベース
            column_names = [field.name for field in table.schema]
            if "ml_generate_embedding_result" in column_names:
                suggestions.append("Vertex AI Embedding APIの結果を格納するテーブル")
            if "content" in column_names and "text" in column_names:
                suggestions.append("テキストコンテンツとその処理結果を格納するテーブル")

            # パターン3: 汎用的な説明
            suggestions.append(f"{dataset_id}データセット内の{table_name}テーブル")

            result = {
                "project_id": project_id,
                "dataset_id": dataset_id,
                "table_name": table_name,
                "current_description": table.description or "",
                "suggested_descriptions": suggestions,
                "table_info": {
                    "table_type": str(table.table_type),
                    "column_count": len(table.schema),
                    "columns": [
                        {"name": field.name, "type": field.field_type}
                        for field in table.schema[:5]
                    ],  # 最初の5列のみ
                    "size_mb": round((table.num_bytes or 0) / 1024 / 1024, 2),
                    "row_count": table.num_rows or 0,
                },
                "sample_data": sample_data,
                "sample_data_count": len(sample_data),
            }

            logger.info(f"✅ 説明提案完了: {dataset_id}.{table_name}")
            return json.dumps(result, indent=2, ensure_ascii=False)

        except Exception as e:
            error_message = f"説明提案エラー: {str(e)}"
            logger.error(f"❌ {error_message}")
            return json.dumps(
                {
                    "error": error_message,
                    "project_id": project_id,
                    "dataset_id": dataset_id,
                    "table_name": table_name,
                }
            )

    async def check_column_descriptions(
        self, project_id: str, dataset_id: str, table_name: str
    ) -> str:
        """
        特定テーブルのカラム説明（論理名）を確認

        Args:
            project_id: プロジェクトID
            dataset_id: データセットID
            table_name: テーブル名

        Returns:
            str: カラム説明情報（JSON形式）
        """
        try:
            logger.info(f"🔄 カラム説明確認開始: {dataset_id}.{table_name}")

            # BigQuery クライアント初期化
            client = bigquery.Client(project=project_id)

            # テーブル取得
            table_ref = client.dataset(dataset_id).table(table_name)
            table = client.get_table(table_ref)

            # カラム情報を詳細に取得
            columns_with_description = []
            columns_without_description = []

            for field in table.schema:
                column_detail = {
                    "name": field.name,
                    "type": field.field_type,
                    "mode": field.mode,
                    "description": field.description or "",
                }

                if field.description:
                    columns_with_description.append(column_detail)
                else:
                    columns_without_description.append(column_detail)

            result = {
                "project_id": project_id,
                "dataset_id": dataset_id,
                "table_name": table_name,
                "table_info": {
                    "has_labels": bool(table.labels),
                    "labels": dict(table.labels) if table.labels else {},
                    "label_count": len(table.labels) if table.labels else 0,
                    "table_type": str(table.table_type),
                    "created": table.created.isoformat() if table.created else None,
                    "description": table.description or "",
                },
                "total_columns": len(table.schema),
                "columns_with_description": columns_with_description,
                "columns_without_description": columns_without_description,
                "columns_with_description_count": len(columns_with_description),
                "columns_without_description_count": len(columns_without_description),
                "description_coverage_percent": round(
                    (len(columns_with_description) / len(table.schema)) * 100, 1
                )
                if table.schema
                else 0,
            }

            logger.info(f"✅ カラム説明確認完了: {dataset_id}.{table_name}")
            return json.dumps(result, indent=2, ensure_ascii=False)

        except Exception as e:
            error_message = f"カラム説明確認エラー: {str(e)}"
            logger.error(f"❌ {error_message}")
            return json.dumps(
                {
                    "error": error_message,
                    "project_id": project_id,
                    "dataset_id": dataset_id,
                    "table_name": table_name,
                }
            )

    async def get_table_lineage(
        self, project_id: str, dataset_id: str, table_id: str
    ) -> str:
        """
        BigQuery Information Schemaを使用してテーブルの依存関係（リネージ）を取得

        Args:
            project_id: プロジェクトID
            dataset_id: データセットID
            table_id: テーブルID

        Returns:
            str: リネージ情報（JSON形式）
        """
        try:
            logger.info(
                f"🔍 テーブルリネージ取得開始: {project_id}.{dataset_id}.{table_id}"
            )

            # BigQuery Information Schemaを使用してリネージを取得
            upstream_deps = await self._get_upstream_dependencies(
                project_id, dataset_id, table_id
            )
            downstream_deps = await self._get_downstream_dependencies(
                project_id, dataset_id, table_id
            )
            table_info = await self._get_table_basic_info(
                project_id, dataset_id, table_id
            )

            lineage_info = {
                "target_table": table_info,
                "upstream_dependencies": upstream_deps,
                "downstream_dependencies": downstream_deps,
                "data_flow_summary": {
                    "total_upstream_entities": len(upstream_deps),
                    "total_downstream_entities": len(downstream_deps),
                    "data_sources": [
                        dep.get("table_name", "") for dep in upstream_deps
                    ],
                    "data_destinations": [
                        dep.get("table_name", "") for dep in downstream_deps
                    ],
                },
                "lineage_metadata": {
                    "api_source": "BigQuery Information Schema",
                    "retrieved_at": datetime.now().isoformat(),
                    "note": "INFORMATION_SCHEMA.TABLE_DEPENDENCIES使用",
                },
            }

            logger.info(
                f"✅ テーブルリネージ取得完了: {dataset_id}.{table_id} (上流:{len(upstream_deps)}, 下流:{len(downstream_deps)})"
            )
            return json.dumps(lineage_info, indent=2, ensure_ascii=False)

        except Exception as e:
            error_message = f"テーブルリネージ取得エラー: {str(e)}"
            logger.error(f"❌ {error_message}")
            return json.dumps(
                {
                    "error": error_message,
                    "project_id": project_id,
                    "dataset_id": dataset_id,
                    "table_id": table_id,
                }
            )

    async def _get_upstream_dependencies(
        self, project_id: str, dataset_id: str, table_id: str
    ) -> list:
        """上流依存関係を取得"""
        try:
            # まずINFORMATION_SCHEMA.TABLE_DEPENDENCIESを試行
            # クエリ履歴から上流依存関係を分析
            query = f"""
            SELECT DISTINCT
                referenced_table.project_id as source_project,
                referenced_table.dataset_id as source_dataset,
                referenced_table.table_id as source_table,
                CONCAT(referenced_table.project_id, '.', referenced_table.dataset_id, '.', referenced_table.table_id) as table_name,
                'BigQuery Table' as entity_type,
                'Query History Analysis' as relationship_type,
                COUNT(*) as reference_count
            FROM `{project_id}.region-asia-northeast1.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
            CROSS JOIN UNNEST(referenced_tables) as referenced_table
            WHERE destination_table.project_id = '{project_id}'
              AND destination_table.dataset_id = '{dataset_id}'
              AND destination_table.table_id = '{table_id}'
              AND creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
              AND job_type = 'QUERY'
              AND state = 'DONE'
              AND referenced_table.project_id IS NOT NULL
            GROUP BY 1, 2, 3, 4, 5, 6
            ORDER BY reference_count DESC
            LIMIT 50
            """

            # BigQuery クライアント初期化
            client = bigquery.Client(project=project_id)
            query_job = client.query(query)
            results = query_job.result()

            return [dict(row) for row in results]

        except Exception as e:
            logger.warning(f"上流依存関係取得エラー: {e}")
            return []

    async def _get_downstream_dependencies(
        self, project_id: str, dataset_id: str, table_id: str
    ) -> list:
        """下流依存関係を取得"""
        try:
            # クエリ履歴から下流依存関係を分析
            query = f"""
            SELECT DISTINCT
                destination_table.project_id as target_project,
                destination_table.dataset_id as target_dataset,
                destination_table.table_id as target_table,
                CONCAT(destination_table.project_id, '.', destination_table.dataset_id, '.', destination_table.table_id) as table_name,
                'BigQuery Table' as entity_type,
                'Query History Analysis' as relationship_type,
                COUNT(*) as reference_count
            FROM `{project_id}.region-asia-northeast1.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
            CROSS JOIN UNNEST(referenced_tables) as referenced_table
            WHERE referenced_table.project_id = '{project_id}'
              AND referenced_table.dataset_id = '{dataset_id}'
              AND referenced_table.table_id = '{table_id}'
              AND creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
              AND job_type = 'QUERY'
              AND state = 'DONE'
              AND destination_table.project_id IS NOT NULL
            GROUP BY 1, 2, 3, 4, 5, 6
            ORDER BY reference_count DESC
            LIMIT 50
            """

            # BigQuery クライアント初期化
            client = bigquery.Client(project=project_id)

            # クエリ実行
            query_job = client.query(query)
            result = query_job.result()

            return [dict(row) for row in result] if result else []

        except Exception as e:
            logger.warning(f"下流依存関係取得エラー: {e}")
            return []

    async def _get_table_basic_info(
        self, project_id: str, dataset_id: str, table_id: str
    ) -> dict:
        """テーブル基本情報を取得"""
        try:
            query = f"""
            SELECT
                table_catalog as project_id,
                table_schema as dataset_id,
                table_name as table_id,
                CONCAT(table_catalog, '.', table_schema, '.', table_name) as full_name,
                table_type,
                creation_time,
                ddl
            FROM `{project_id}.{dataset_id}.INFORMATION_SCHEMA.TABLES`
            WHERE table_schema = '{dataset_id}'
              AND table_name = '{table_id}'
            """

            # BigQuery クライアント初期化
            client = bigquery.Client(project=project_id)

            # クエリ実行
            query_job = client.query(query)
            result = query_job.result()

            if result:
                row_dict = dict(list(result)[0])
                # datetime オブジェクトをISO文字列に変換
                if "creation_time" in row_dict and row_dict["creation_time"]:
                    row_dict["creation_time"] = row_dict["creation_time"].isoformat()
                return row_dict
            else:
                return {
                    "project_id": project_id,
                    "dataset_id": dataset_id,
                    "table_id": table_id,
                    "full_name": f"{project_id}.{dataset_id}.{table_id}",
                    "table_type": "Unknown",
                    "note": "テーブル情報取得失敗",
                }

        except Exception as e:
            logger.warning(f"テーブル情報取得エラー: {e}")
            return {
                "project_id": project_id,
                "dataset_id": dataset_id,
                "table_id": table_id,
                "full_name": f"{project_id}.{dataset_id}.{table_id}",
                "error": str(e),
            }

    async def calculate_governance_score(
        self, project_id: str, dataset_id: str, table_id: str
    ) -> dict:
        """
        単一テーブルのガバナンススコアを計算

        Args:
            project_id: プロジェクトID
            dataset_id: データセットID
            table_id: テーブルID

        Returns:
            dict: ガバナンススコア結果
        """
        try:
            client = bigquery.Client(project=project_id)
            score_result = await self._calculate_single_table_score(
                client, project_id, dataset_id, table_id
            )

            return {
                "table_score": score_result,
                "analysis_metadata": {
                    "analyzed_at": datetime.now().isoformat(),
                    "scope": f"project:{project_id}, dataset:{dataset_id}, table:{table_id}",
                },
            }

        except Exception as e:
            logger.error(f"ガバナンススコア計算エラー: {e}")
            return {
                "error": f"ガバナンススコア計算に失敗しました: {str(e)}",
                "analysis_metadata": {
                    "analyzed_at": datetime.now().isoformat(),
                    "scope": f"project:{project_id}, dataset:{dataset_id}, table:{table_id}",
                },
            }

    async def _calculate_single_table_score(
        self, client: bigquery.Client, project_id: str, dataset_id: str, table_id: str
    ) -> dict:
        """単一テーブルのガバナンススコアを計算"""
        try:
            score_details = {
                "table_info": {
                    "project_id": project_id,
                    "dataset_id": dataset_id,
                    "table_id": table_id,
                    "full_name": f"{project_id}.{dataset_id}.{table_id}",
                },
                "scores": {},
                "total_score": 0,
                "grade": "",
                "issues": [],
            }

            # 1. テーブル説明チェック (25点) - BigQuery APIで取得
            description_score = 0
            try:
                # BigQuery APIでテーブル情報を取得
                table_ref = client.dataset(dataset_id).table(table_id)
                table = client.get_table(table_ref)

                if table.description:
                    desc_length = len(table.description.strip())
                    if desc_length >= 50:
                        description_score = 25
                    elif desc_length >= 20:
                        description_score = 15
                    elif desc_length >= 5:
                        description_score = 10
                    else:
                        score_details["issues"].append(
                            "テーブル説明が短すぎます（5文字未満）"
                        )
                else:
                    score_details["issues"].append("テーブル説明が設定されていません")
            except Exception as e:
                logger.warning(f"テーブル説明取得エラー: {e}")
                score_details["issues"].append("テーブル説明が設定されていません")

            score_details["scores"]["description"] = description_score

            # 2. 論理名（ラベル）チェック (20点) - BigQuery APIで取得
            logical_name_score = 0
            business_value_score = 0
            data_classification_score = 0
            has_logical_name = False
            has_business_labels = False
            has_data_classification = False

            try:
                # BigQuery APIでラベル情報を取得（上記で取得済みのtableオブジェクトを使用）
                if hasattr(table, "labels") and table.labels:
                    labels_dict = table.labels

                    # 論理名チェック
                    if "logical_name" in labels_dict:
                        logical_name_score = 20
                        has_logical_name = True

                    # ビジネス価値ラベルチェック
                    if any(
                        key in labels_dict
                        for key in [
                            "business_critical",
                            "business_value",
                            "data_quality",
                        ]
                    ):
                        business_value_score = 15
                        has_business_labels = True

                    # データ分類ラベルチェック
                    if any(
                        key in labels_dict
                        for key in ["pii_data", "data_type", "sensitivity"]
                    ):
                        data_classification_score = 10
                        has_data_classification = True
            except Exception as e:
                logger.warning(f"ラベル取得エラー: {e}")

            if not has_logical_name:
                score_details["issues"].append(
                    "論理名（logical_nameラベル）が設定されていません"
                )

            score_details["scores"]["logical_name"] = logical_name_score

            # 3. カラム説明チェック (30点) - BigQuery APIで取得
            column_score = 0
            try:
                # BigQuery APIでスキーマ情報を取得（上記で取得済みのtableオブジェクトを使用）
                if hasattr(table, "schema") and table.schema:
                    total_columns = len(table.schema)
                    described_columns = len(
                        [field for field in table.schema if field.description]
                    )
                    column_coverage = (
                        described_columns / total_columns if total_columns > 0 else 0
                    )

                    if column_coverage >= 0.9:
                        column_score = 30
                    elif column_coverage >= 0.7:
                        column_score = 20
                    elif column_coverage >= 0.5:
                        column_score = 15
                    elif column_coverage >= 0.3:
                        column_score = 10
                    else:
                        score_details["issues"].append(
                            f"カラム説明の設定率が低いです（{described_columns}/{total_columns} = {column_coverage:.1%}）"
                        )
                else:
                    score_details["issues"].append("カラム情報を取得できませんでした")
            except Exception as e:
                logger.warning(f"カラム説明取得エラー: {e}")
                score_details["issues"].append("カラム説明を取得できませんでした")

            score_details["scores"]["column_descriptions"] = column_score

            # 4. ビジネス価値ラベル・データ分類ラベルのスコア設定（上記で計算済み）
            if not has_business_labels:
                score_details["issues"].append(
                    "ビジネス価値関連ラベル（business_critical, business_value, data_quality）が設定されていません"
                )

            if not has_data_classification:
                score_details["issues"].append(
                    "データ分類ラベル（pii_data, data_type, sensitivity）が設定されていません"
                )

            score_details["scores"]["business_labels"] = business_value_score
            score_details["scores"]["data_classification"] = data_classification_score

            # 総合スコア計算
            total_score = (
                description_score
                + logical_name_score
                + column_score
                + business_value_score
                + data_classification_score
            )

            # グレード判定
            if total_score >= 90:
                grade = "ランクA"
            elif total_score >= 70:
                grade = "ランクB"
            elif total_score >= 50:
                grade = "ランクC"
            else:
                grade = "ランクD"

            score_details["total_score"] = total_score
            score_details["grade"] = grade

            return score_details

        except Exception as e:
            logger.error(f"単一テーブルスコア計算エラー: {e}")
            return {
                "table_info": {
                    "project_id": project_id,
                    "dataset_id": dataset_id,
                    "table_id": table_id,
                },
                "error": str(e),
                "total_score": 0,
                "grade": "F",
            }

    async def get_table_statistics(
        self, project_id: str, dataset_id: str, table_id: str
    ) -> dict:
        """
        テーブルのカラム統計情報を取得（データ品質分析用）

        Args:
            project_id: プロジェクトID
            dataset_id: データセットID
            table_id: テーブルID

        Returns:
            dict: カラム統計情報
        """
        try:
            client = bigquery.Client(project=project_id)

            # テーブル基本情報取得
            table_ref = client.dataset(dataset_id).table(table_id)
            table = client.get_table(table_ref)

            statistics = {
                "table_info": {
                    "project_id": project_id,
                    "dataset_id": dataset_id,
                    "table_id": table_id,
                    "full_name": f"{project_id}.{dataset_id}.{table_id}",
                    "num_rows": table.num_rows,
                    "num_bytes": table.num_bytes,
                },
                "column_statistics": [],
            }

            # カラム統計情報取得のみ
            for field in table.schema:
                column_stats = await self._analyze_column_statistics(
                    client, project_id, dataset_id, table_id, field
                )
                statistics["column_statistics"].append(column_stats)

            return statistics

        except Exception as e:
            logger.error(f"テーブル統計情報取得エラー: {e}")
            return {
                "error": f"統計情報取得に失敗しました: {str(e)}",
                "table_info": {
                    "project_id": project_id,
                    "dataset_id": dataset_id,
                    "table_id": table_id,
                },
            }

    async def _analyze_column_statistics(
        self,
        client: bigquery.Client,
        project_id: str,
        dataset_id: str,
        table_id: str,
        field,
    ) -> dict:
        """カラム統計情報を分析"""
        try:
            # NULL率計算
            null_query = f"""
            SELECT
                COUNT(*) as total_count,
                COUNTIF({field.name} IS NULL) as null_count,
                ROUND(COUNTIF({field.name} IS NULL) / COUNT(*) * 100, 2) as null_percentage
            FROM `{project_id}.{dataset_id}.{table_id}`
            """

            null_result = list(client.query(null_query).result())[0]

            column_stats = {
                "column_name": field.name,
                "data_type": field.field_type,
                "mode": field.mode,
                "description": field.description or "",
                "total_count": null_result.total_count,
                "null_count": null_result.null_count,
                "null_percentage": null_result.null_percentage,
                "non_null_count": null_result.total_count - null_result.null_count,
            }

            # 数値型の場合の統計情報
            if field.field_type in ["INTEGER", "FLOAT", "NUMERIC"]:
                numeric_query = f"""
                SELECT
                    MIN({field.name}) as min_value,
                    MAX({field.name}) as max_value,
                    AVG({field.name}) as avg_value,
                    STDDEV({field.name}) as stddev_value,
                    APPROX_QUANTILES({field.name}, 4)[OFFSET(2)] as median_value
                FROM `{project_id}.{dataset_id}.{table_id}`
                WHERE {field.name} IS NOT NULL
                """
                numeric_result = list(client.query(numeric_query).result())[0]
                column_stats.update(
                    {
                        "min_value": float(numeric_result.min_value)
                        if numeric_result.min_value is not None
                        else None,
                        "max_value": float(numeric_result.max_value)
                        if numeric_result.max_value is not None
                        else None,
                        "avg_value": float(numeric_result.avg_value)
                        if numeric_result.avg_value is not None
                        else None,
                        "stddev_value": float(numeric_result.stddev_value)
                        if numeric_result.stddev_value is not None
                        else None,
                        "median_value": float(numeric_result.median_value)
                        if numeric_result.median_value is not None
                        else None,
                    }
                )

            # 文字列型の場合の統計情報
            elif field.field_type == "STRING":
                string_query = f"""
                SELECT
                    MIN(LENGTH({field.name})) as min_length,
                    MAX(LENGTH({field.name})) as max_length,
                    AVG(LENGTH({field.name})) as avg_length,
                    COUNT(DISTINCT {field.name}) as distinct_count
                FROM `{project_id}.{dataset_id}.{table_id}`
                WHERE {field.name} IS NOT NULL
                """
                string_result = list(client.query(string_query).result())[0]
                column_stats.update(
                    {
                        "min_length": string_result.min_length,
                        "max_length": string_result.max_length,
                        "avg_length": float(string_result.avg_length)
                        if string_result.avg_length is not None
                        else None,
                        "distinct_count": string_result.distinct_count,
                        "distinct_ratio": string_result.distinct_count
                        / column_stats["non_null_count"]
                        if column_stats["non_null_count"] > 0
                        else 0,
                    }
                )

            return column_stats

        except Exception as e:
            logger.warning(f"カラム統計分析エラー ({field.name}): {e}")
            return {
                "column_name": field.name,
                "data_type": field.field_type,
                "error": str(e),
            }
