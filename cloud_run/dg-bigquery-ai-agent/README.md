# DG BigQuery AI Agent

Google Cloud BigQuery専用AIエージェント - MCP統合

## 📋 概要

DG BigQuery AI Agentは、Google Cloud BigQueryに特化したAIエージェントです。dg-data-governance-agentの子エージェントとして動作し、BigQueryに関する専門的な質問に対してリアルタイムでデータを取得・分析します。

### 主な機能

- **BigQueryデータセット一覧取得**: プロジェクト内のデータセット情報を取得
- **BigQueryテーブル詳細取得**: テーブル構造・メタデータの詳細分析
- **BigQueryクエリ実行**: 安全なクエリ実行とデータ分析
- **セキュリティガードレール**: 危険な操作の防止と監査ログ記録
- **A2A通信対応**: 親エージェントからの委譲処理に最適化

## 🏗️ アーキテクチャ

```text
dg-data-governance-agent (親エージェント)
    ↓ A2A通信
dg-bigquery-ai-agent (子エージェント)
    ↓ MCP通信
dg-bigquery-mcp-server (MCPサーバー)
    ↓ API呼び出し
Google Cloud BigQuery API
```

## 🚀 セットアップ

### 前提条件

- Python 3.12以上
- Poetry 2.1.1
- Docker
- Google Cloud SDK
- 適切なGoogle Cloud権限

### ローカル開発

```bash
# 依存関係インストール
poetry install

# 環境変数設定
export MCP_SERVER_URL="https://dg-bigquery-mcp-server-xxx.run.app"
export GOOGLE_CLOUD_PROJECT="your-project-id"

# アプリケーション起動
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Cloud Runデプロイ

```bash
# デプロイ実行
./deploy.sh <PROJECT_ID> <SERVICE_ACCOUNT>

# 例
./deploy.sh your-project-id sample-service-account@your-project-id.iam.gserviceaccount.com
```

## 🔧 利用可能なツール

### 1. get_bigquery_datasets

BigQueryデータセット一覧を取得します。

**パラメータ:**

- `project_id` (str): 対象プロジェクトID（デフォルト: your-project-id）

### 2. get_bigquery_tables

BigQueryテーブル一覧・詳細を取得します。

**パラメータ:**

- `project_id` (str): 対象プロジェクトID（デフォルト: your-project-id）
- `dataset_id` (str): 対象データセットID

### 3. execute_bigquery_query

BigQueryクエリを実行します。

**パラメータ:**

- `project_id` (str): 対象プロジェクトID（デフォルト: your-project-id）
- `query` (str): 実行するSQLクエリ

## 🛡️ セキュリティ機能

### ガードレール機能

1. **プロジェクト制限**: 本番環境での危険なproject_idへのアクセス制限
2. **操作制限**: 削除・変更系操作の実行防止
3. **機密データ保護**: 機密情報へのアクセス制御
4. **クエリ検証**: 危険なクエリパターンの検出と防止
5. **監査ログ**: 全ツール実行の詳細ログ記録

### 制限事項

- 読み取り専用クエリのみ実行可能
- DROP、DELETE、TRUNCATE等の危険な操作は禁止
- 機密データを含む引数の使用制限

## 📡 API エンドポイント

### POST /chat

AIエージェントとのチャットエンドポイント

**リクエスト:**

```json
{
  "message": "BigQueryのデータセット一覧を教えて",
  "session_id": "optional-session-id"
}
```

**レスポンス:**

```json
{
  "response": "以下がBigQueryデータセット一覧です...",
  "session_id": "session-id",
  "tools_used": ["get_bigquery_datasets"]
}
```

### GET /health

ヘルスチェックエンドポイント

**レスポンス:**

```json
{
  "status": "healthy",
  "service": "dg-bigquery-ai-agent",
  "version": "1.0.0",
  "agent_status": "ready",
  "mcp_server_connected": true
}
```

## 🔗 親エージェント連携

dg-data-governance-agentから以下のパターンで呼び出されます：

1. **BigQuery関連キーワード検出**: "bigquery", "テーブル", "データセット", "クエリ"等
2. **A2A通信**: 認証済みHTTPSリクエストで委譲
3. **結果統合**: 技術的分析結果を親エージェントに返却

## 🚀 デプロイメント

### 環境変数

| 変数名 | 説明 | 必須 |
|--------|------|------|
| `MCP_SERVER_URL` | BigQuery MCPサーバーのURL | Yes |
| `GOOGLE_CLOUD_PROJECT` | Google CloudプロジェクトID | Yes |
| `ADK_DEBUG` | Google ADKデバッグモード | No |

### Cloud Run設定

- **CPU**: 1 vCPU
- **メモリ**: 2Gi
- **最大インスタンス数**: 10
- **リクエストタイムアウト**: 300秒

## 📄 ライセンス

Copyright (c) 2025 Sample Organization
