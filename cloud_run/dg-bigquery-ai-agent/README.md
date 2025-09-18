# DG BigQuery AI Agent

Google Cloud BigQuery専用AIエージェント - MCP統合

## 📋 概要

DG BigQuery AI Agentは、Google Cloud BigQueryに特化したAIエージェントです。dg-data-governance-agentの子エージェントとして動作し、BigQueryに関する専門的な質問に対してリアルタイムでデータを取得・分析します。

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

## 🔧 主要機能

### MCPサーバー経由で提供

このエージェントは `dg-bigquery-mcp-server` を通じて以下の機能を提供します：

- **BigQueryデータセット一覧取得**: プロジェクト内のデータセット情報を取得
- **BigQueryテーブル詳細取得**: テーブル構造・メタデータの詳細分析
- **BigQueryクエリ実行**: 安全なクエリ実行とデータ分析
- **セキュリティガードレール**: 危険な操作の防止と監査ログ記録
- **A2A通信対応**: 親エージェントからの委譲処理に最適化

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

## 🚀 デプロイ

```bash
# デプロイ実行
./deploy.sh <PROJECT_ID> <SERVICE_ACCOUNT>

# 例
./deploy.sh your-project-id your-service-account@your-project-id.iam.gserviceaccount.com
```

## 📊 技術スタック

- **Python 3.12+**: プログラミング言語
- **Poetry 2.1.1**: 依存関係管理（バージョン固定）
- **Google ADK**: AIエージェント開発キット
- **FastAPI**: Webフレームワーク
- **Google Cloud Platform**:
  - Cloud Run
  - BigQuery API
  - Vertex AI

## 🔗 関連サービス

- **dg-data-governance-agent**: 親エージェント（このエージェントを呼び出し）
- **dg-bigquery-mcp-server**: BigQuery API統合サーバー（このエージェントが使用）
