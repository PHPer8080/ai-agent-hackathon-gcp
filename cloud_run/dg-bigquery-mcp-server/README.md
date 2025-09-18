# DG BigQuery MCP Server

BigQuery専用MCPサーバー - データガバナンス機能

## 📋 概要

BigQuery MCP Serverは、BigQueryのデータガバナンス機能を提供するMCPサーバーです。
dg-bigquery-ai-agentと連携し、BigQueryデータセット・テーブルの管理とガバナンス機能を提供します。

## 🔧 主要機能

- **データセット一覧取得**: BigQueryプロジェクト内のデータセット一覧を取得
- **テーブル詳細取得**: テーブル構造・メタデータの詳細分析
- **クエリ実行**: 安全なBigQueryクエリの実行
- **データガバナンス**: テーブル説明・ラベル不足の検出と優先度付け

## 🏗️ アーキテクチャ

```text
dg-bigquery-ai-agent → dg-bigquery-mcp-server → BigQuery API
```

## 📡 API エンドポイント

### ヘルスチェック

```bash
GET /health
```

### BigQuery操作

```bash
# データセット一覧取得
POST /bigquery/datasets
{
  "project_id": "your-project-id"
}

# テーブル詳細取得
POST /bigquery/tables
{
  "project_id": "your-project-id",
  "dataset_id": "tt_hackathon"
}

# クエリ実行
POST /bigquery/query
{
  "project_id": "your-project-id",
  "query": "SELECT * FROM `project.dataset.table` LIMIT 10"
}
```

## 🚀 デプロイ

```bash
./deploy.sh <PROJECT_ID> <SERVICE_ACCOUNT>

# 例
./deploy.sh your-project-id sample-service-account@your-project-id.iam.gserviceaccount.com
```

## ⚙️ 技術スタック

- **FastAPI**: Webフレームワーク
- **fastapi-mcp**: MCP統合
- **google-cloud-bigquery**: BigQuery API
- **Poetry 2.1.1**: 依存関係管理

## 🔒 セキュリティ

- 非rootユーザーでの実行
- 最小権限の原則
- 認証トークンによるアクセス制御
- 読み取り専用クエリのみ許可

## 🔗 関連サービス

- **dg-bigquery-ai-agent**: BigQuery専用AIエージェント（このMCPサーバーを使用）
- **dg-data-governance-agent**: 親エージェント（間接連携）
