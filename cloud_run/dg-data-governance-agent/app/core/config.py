"""
データガバナンスエージェント共通設定

エージェント間で共有される設定とキーワード判定ロジックを管理
"""

import logging
import os
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class AgentConfig:
    """エージェント設定クラス"""

    # アプリケーション設定
    APP_NAME = "dg_data_governance_agent"

    # Dataplex専用キーワード（BigQueryエージェントでは除外対象）
    # fmt: off
    DATAPLEX_EXCLUSIVE_KEYWORDS = [
        "dataplex", "データレイク", "data lake", "アセット", "asset", "系譜", "lineage",
        "データ系譜", "リネージ", "依存関係", "依存", "上流", "下流", "upstream", "downstream",
        "データフロー", "data flow", "関係性", "関連"
    ]
    # fmt: on

    # Dataplexエージェント委譲用キーワード（データ品質専用）
    # fmt: off
    DATAPLEX_KEYWORDS = ["dataplex", "データレイク", "アセット"]
    # fmt: on

    # データ品質シーケンシャル実行キーワード（BigQuery統計→Dataplex提案）
    # fmt: off
    DATA_QUALITY_SEQUENTIAL_KEYWORDS = [
        "データ品質", "品質ルール", "品質改善", "品質分析", "品質提案", "改善提案", "品質向上",
        "data quality", "quality rule", "quality improvement", "quality analysis", "quality suggestion",
        "ガバナンススコア", "governance score", "品質スコア", "quality score", "品質評価", "quality evaluation",
        "品質測定", "quality measurement", "品質監視", "quality monitoring", "品質管理", "quality management",
        "品質保証", "quality assurance", "品質チェック", "quality check", "品質検証", "quality validation",
        "品質基準", "quality standard", "品質指標", "quality metric", "品質レポート", "quality report",
        "品質ダッシュボード", "quality dashboard", "品質アラート", "quality alert", "品質しきい値", "quality threshold",
        "データプロファイリング", "data profiling", "統計情報", "statistics", "データ統計", "data statistics",
        "テーブル統計", "table statistics", "カラム統計", "column statistics", "データ分布", "data distribution",
        "null値", "null value", "欠損値", "missing value", "重複", "duplicate", "一意性", "uniqueness",
        "整合性", "consistency", "完全性", "completeness", "正確性", "accuracy", "妥当性", "validity",
        "適時性", "timeliness", "関連性", "relevance", "信頼性", "reliability", "可用性", "availability"
    ]
    # fmt: on

    # BigQuery明示的キーワード（必ずBigQueryエージェントに委譲）
    # fmt: off
    BIGQUERY_EXPLICIT_KEYWORDS = [
        "bigquery", "bq", "sql", "クエリ", "query", "テーブル", "table", "カラム", "column",
        "データセット", "dataset", "スキーマ", "schema", "メタデータ", "metadata", "説明", "description",
        "論理名", "logical name", "ラベル", "label", "タグ", "tag", "分析", "analysis",
        "集計", "aggregation", "グループ化", "grouping", "結合", "join", "フィルタ", "filter",
        "ソート", "sort", "並び替え", "order", "検索", "search", "取得", "retrieve",
        "抽出", "extract", "変換", "transform", "加工", "process", "計算", "calculate",
        "算出", "compute", "合計", "sum", "平均", "average", "最大", "max", "最小", "min",
        "件数", "count", "行数", "rows", "レコード", "record", "データ", "data", "値", "value",
        "フィールド", "field", "インデックス", "index", "パーティション", "partition", "クラスタ", "cluster",
        "ビュー", "view", "マテリアライズドビュー", "materialized view", "ストアドプロシージャ", "stored procedure",
        "関数", "function", "UDF", "user defined function", "ジョブ", "job", "実行", "execute",
        "処理", "process", "バッチ", "batch", "ストリーミング", "streaming", "リアルタイム", "realtime",
        "スケジュール", "schedule", "自動化", "automation", "パフォーマンス", "performance", "最適化", "optimization",
        "コスト", "cost", "料金", "pricing", "容量", "capacity", "ストレージ", "storage",
        "圧縮", "compression", "暗号化", "encryption", "セキュリティ", "security", "権限", "permission",
        "アクセス", "access", "認証", "authentication", "認可", "authorization", "監査", "audit",
        "ログ", "log", "モニタリング", "monitoring", "アラート", "alert", "バックアップ", "backup",
        "復元", "restore", "レプリケーション", "replication", "同期", "sync", "移行", "migration",
        "インポート", "import", "エクスポート", "export", "連携", "integration", "API", "REST",
        "GraphQL", "JDBC", "ODBC", "SDK", "ライブラリ", "library", "ツール", "tool",
        "クライアント", "client", "ドライバ", "driver", "接続", "connection", "エンドポイント", "endpoint",
        "プロトコル", "protocol", "フォーマット", "format", "JSON", "CSV", "Parquet", "Avro", "ORC"
    ]
    # fmt: on

    # あいまいな疑問詞（親エージェントが直接処理）
    # fmt: off
    AMBIGUOUS_QUESTION_WORDS = [
        "何", "なに", "なん", "どこ", "いつ", "だれ", "誰", "どう", "どのように", "なぜ",
        "why", "how", "what", "where", "when", "who", "どんな", "いくつ", "どのくらい",
        "教えて", "知りたい", "見せて", "確認", "チェック"
    ]
    # fmt: on

    # あいまいな短い疑問文
    # fmt: off
    AMBIGUOUS_SHORT_QUESTIONS = ["?", "？", "何？", "なに？", "どう？", "how?", "what?"]
    # fmt: on

    # プロジェクト関連キーワード
    # fmt: off
    PROJECT_KEYWORDS = [
        "プロジェクト", "project", "tt_us",
        "データレイク", "データウェアハウス", "ユーザーストレージ"
    ]
    # fmt: on

    # データ関連キーワード
    # fmt: off
    DATA_KEYWORDS = ["データ", "data", "情報", "information", "レコード", "record", "ファイル", "file"]
    # fmt: on

    # アクション関連キーワード
    # fmt: off
    ACTION_KEYWORDS = ["取得", "get", "検索", "search", "確認", "check", "分析", "analyze", "処理", "process"]
    # fmt: on

    # ガバナンス関連キーワード
    # fmt: off
    GOVERNANCE_KEYWORDS = ["ガバナンス", "governance", "管理", "management", "制御", "control", "ポリシー", "policy"]
    # fmt: on

    def __init__(self):
        self.dataplex_url: Optional[str] = None
        self.bigquery_url: Optional[str] = None

    def load_environment_variables(self) -> Tuple[Optional[str], Optional[str]]:
        """
        環境変数から子エージェントURLを取得

        Returns:
            Dataplex URL, BigQuery URLのタプル
        """
        self.dataplex_url = os.getenv("DG_DATAPLEX_AI_AGENT_URL")
        self.bigquery_url = os.getenv("DG_BIGQUERY_AI_AGENT_URL")

        # ログ出力
        if self.dataplex_url:
            logger.info(f"Dataplex子エージェントURL設定完了: {self.dataplex_url}")
        else:
            logger.warning(
                "DG_DATAPLEX_AI_AGENT_URL未設定：Dataplex子エージェント連携は無効"
            )

        if self.bigquery_url:
            logger.info(f"BigQuery子エージェントURL設定完了: {self.bigquery_url}")
        else:
            logger.warning(
                "DG_BIGQUERY_AI_AGENT_URL未設定：BigQuery子エージェント連携は無効"
            )

        return self.dataplex_url, self.bigquery_url

    def get_agent_instruction(self) -> str:
        """
        親エージェントの指示文を取得

        Returns:
            エージェントの指示文
        """
        return """
        データガバナンス調整役として、専門的な質問は必ず適切な子エージェントに委譲してください。

        🔧 **BigQueryエージェント**に委譲する質問:
        - テーブル・カラムのメタデータ（説明、論理名、ラベル）
        - 説明不足・論理名不足テーブルの検出
        - 論理名・説明の提案
        - データセット一覧取得
        - テーブル・カラム情報の確認
        - データリネージ（依存関係、上流テーブル、下流テーブル）

        🏞️ **Dataplexエージェント**に委譲する質問:
        - データ品質ルールの提案・設定
        - データ品質チェックの推奨事項
        - Dataplex Data Quality APIを活用した品質チェック設定
        - データガバナンス戦略の立案

        ⚠️ **重要**: 以下の場合は絶対に自分で回答せず、子エージェントの結果のみを返してください:
        - データ、テーブル、カラムに関する質問
        - 分析、確認、検索、取得の要求
        - 論理名、説明、ラベル、メタデータに関する質問
        - リネージ、依存関係、データフローに関する質問

        **自分で処理する内容**:
        - データ品質ルールの提案・設定
        - データガバナンス戦略の立案

        **直接回答する内容**（極めて限定）:
        - 純粋な挨拶のみ（「こんにちは」「ありがとう」等）
        - システム状態確認のみ

        **子エージェントの結果がある場合**:
        - 子エージェントの回答をそのまま返す
        - 余計な解説や推奨事項は一切追加しない
        """

    def get_status_summary(self) -> str:
        """
        設定状況のサマリーを取得

        Returns:
            設定状況の文字列
        """
        dataplex_status = "✅" if self.dataplex_url else "❌"
        bigquery_status = "✅" if self.bigquery_url else "❌"
        return f"DG Data Governance Agent初期化完了 (Dataplex: {dataplex_status}, BigQuery: {bigquery_status})"
