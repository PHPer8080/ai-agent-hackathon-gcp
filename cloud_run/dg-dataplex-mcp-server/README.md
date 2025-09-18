# DG Dataplex MCP Server

Dataplex API統合MCPサーバー - AIエージェント連携

## 📋 概要

Model Context Protocol (MCP) を実装したDataplex専用サーバーです。Google Cloud Dataplex APIと統合し、dg-dataplex-ai-agentと連携してDataplexデータアセット、データ系譜、データ品質メトリクス、タグ管理を提供します。

## 🏗️ アーキテクチャ

```text
dg-dataplex-ai-agent → dg-dataplex-mcp-server → Dataplex API
```

## 🔧 提供ツール

### MCPツール一覧

1. **list-dataplex-assets**: Dataplexデータアセットの一覧取得
2. **get-data-lineage**: データ系譜情報の詳細分析
3. **get-data-quality-metrics**: データ品質メトリクスとルール評価
4. **manage-dataplex-tags**: メタデータタグの管理（CRUD操作）
5. **get-bigquery-metadata**: BigQueryテーブルメタデータ取得（Dataplex API経由）

### 直接APIエンドポイント

- **BigQueryメタデータ取得**: `/dataplex/bigquery/metadata`
- **ヘルスチェック**: `/health`
- **MCP機能一覧**: `/mcp/capabilities`, `/mcp/tools`

## 🚀 デプロイ

```bash
# デプロイスクリプト実行
./deploy.sh <PROJECT_ID> <SERVICE_ACCOUNT>

# 例
./deploy.sh your-project-id your-service-account@your-project-id.iam.gserviceaccount.com
```

### 必要な権限

サービスアカウントには以下のロールが必要です：

- `roles/dataplex.viewer` - Dataplexリソースの読み取り
- `roles/dataplex.metadataReader` - メタデータアクセス
- `roles/dataplex.dataReader` - データ系譜情報アクセス
- `roles/bigquery.metadataViewer` - BigQueryメタデータ読み取り（統合機能用）

## 📊 技術スタック

- **Python 3.12+**: プログラミング言語
- **FastAPI**: 高性能WebAPIフレームワーク
- **Poetry 2.1.1**: 依存関係管理（バージョン固定）
- **Pydantic**: データバリデーション
- **Google Cloud Platform**:
  - Cloud Run
  - Dataplex API
  - Identity & Access Management (IAM)

## 🔗 関連サービス

- **dg-dataplex-ai-agent**: Dataplex専門AIエージェント（このMCPサーバーを使用）
- **dg-data-governance-agent**: 親エージェント（間接連携）
