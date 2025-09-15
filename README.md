# Data Governance AI Agent System

## 🏆 提出作品

Google Cloud Platform上で動作するマルチエージェント構成のデータガバナンスシステムです。BigQueryとDataplexを統合し、AIエージェントによる自動化されたデータ品質管理とガバナンス分析を提供します。

## 🏗️ システム構成

### マルチエージェント アーキテクチャ
- **親エージェント**: 統合的なデータガバナンス分析とエージェント間の調整
- **BigQuery AIエージェント**: BigQueryデータの品質分析、メタデータ管理
- **Dataplex AIエージェント**: Dataplexによるデータ品質ルール提案
- **MCPサーバー**: BigQuery/Dataplex APIとの統合インターフェース
- **Chat UI**: Chainlitベースのユーザーインターフェース

### 主要機能
- 📊 **データセット・テーブル分析**: メタデータ不足の自動検出
- 🏷️ **論理名・説明提案**: AIによる適切なメタデータ生成
- 🔗 **データリネージ分析**: テーブル間の依存関係可視化
- 🛡️ **データ品質ルール提案**: 統計情報に基づく品質チェック設定
- 📈 **ガバナンススコア算出**: 総合的なデータ品質評価
- 🤖 **マルチエージェント連携**: 複数の専門AIエージェントによる協調分析

### 🚀 技術スタック
- **MCP (Model Context Protocol)**: 最新のAIエージェント統合プロトコル
- **A2A (Agent-to-Agent)**: エージェント間の自律的な協調処理
- **Gemini 1.5 Flash**: Google最新LLMによる高速データ分析
- **Cloud Run**: サーバーレスでのスケーラブルなマイクロサービス構成
- **BigQuery**: メタデータとリネージの動的分析
- **Chainlit**: リアルタイムストリーミング対応のモダンChat UI

## 🚀 クイックスタート

### 前提条件
- Google Cloud Platform アカウント
- BigQuery, Dataplex, Cloud Run の有効化
- Python 3.12+

### デプロイ手順
1. 各サービスディレクトリで `./deploy.sh <PROJECT_ID> <SERVICE_ACCOUNT>` を実行
2. 環境変数を設定してサービス間連携を構成
3. Chat UIからデータガバナンス分析を開始

詳細な手順は各サービスのREADMEを参照してください。

## ⚠️ 重要な注意事項

### FIXMEコメントについて
本プロジェクトには `# FIXME: プロジェクトIDを適宜変更` というコメントが含まれています。
**実際にデプロイする際は、これらの箇所を必ず実際のプロジェクトIDに変更してください。**

主な修正箇所：
- `cloud_run/*/app/core/config.py` - デフォルトプロジェクトID
- `cloud_run/*/app/services/*.py` - 各種サービスのデフォルト値

### テストデータについて
`bigquery/test_governance_tables.sql` にはサンプルテーブルが定義されており、デモ・検証用に使用できます。

## 📁 プロジェクト構造

```
├── cloud_run/                    # Cloud Runサービス群
│   ├── dg-data-governance-agent/  # 親エージェント
│   ├── dg-bigquery-ai-agent/      # BigQuery専用エージェント
│   ├── dg-dataplex-ai-agent/      # Dataplex専用エージェント
│   ├── dg-bigquery-mcp-server/    # BigQuery MCPサーバー
│   ├── dg-dataplex-mcp-server/    # Dataplex MCPサーバー
│   └── dg-data-governance-chatui/ # Chainlit Chat UI
└── bigquery/                     # テストデータ・スキーマ
    ├── test_governance_tables.sql # サンプルテーブル定義
    └── README.md                  # テストデータ説明
```

---
**技術スタック**: Python, FastAPI, Chainlit, Google Cloud (BigQuery, Dataplex, Cloud Run)
