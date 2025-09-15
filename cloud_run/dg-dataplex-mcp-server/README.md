# DG Dataplex MCP Server

Dataplex API統合MCPサーバー - AIエージェント連携

## 📋 概要

Model Context Protocol (MCP) を実装したDataplex専用サーバーです。Google Cloud Dataplex APIと統合し、dg-dataplex-ai-agentと連携してDataplexデータアセット、データ系譜、データ品質メトリクス、タグ管理を提供します。

## 🔧 提供ツール

1. **list-dataplex-assets**: Dataplexデータアセットの一覧取得
2. **get-data-lineage**: データ系譜情報の詳細分析
3. **get-data-quality-metrics**: データ品質メトリクスとルール評価
4. **manage-dataplex-tags**: メタデータタグの管理（CRUD操作）
5. **get-bigquery-metadata**: BigQueryテーブルメタデータ取得（Dataplex API経由）

## 🏗️ アーキテクチャ

```text
dg-dataplex-ai-agent → dg-dataplex-mcp-server → Dataplex API
```

## 📡 API エンドポイント

### ヘルスチェック

```http
GET /health
```

**レスポンス例:**

```json
{
  "status": "healthy",
  "service": "dg-dataplex-mcp-server",
  "version": "1.0.0",
  "project_id": "your-project-id",
  "location": "us-central1",
  "dataplex_ready": true
}
```

### MCP機能一覧

```http
GET /mcp/capabilities
GET /mcp/tools
```

### BigQueryメタデータ取得

```http
POST /dataplex/bigquery/metadata
Content-Type: application/json
```

**リクエスト例:**

```json
{
  "dataset_id": "tt_us",
  "table_id": "raw_products"
}
```

### MCPリクエスト処理

```http
POST /mcp/sse
Content-Type: application/json
Authorization: Bearer <identity_token>
```

**リクエスト例:**

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "list-dataplex-assets",
    "arguments": {
      "project_id": "your-project-id",
      "location": "us-central1"
    }
  },
  "id": 1
}
```

## 🚀 デプロイメント

```bash
# デプロイスクリプト実行
./deploy.sh <PROJECT_ID> <SERVICE_ACCOUNT>

# 例
./deploy.sh your-project-id sample-service-account@your-project-id.iam.gserviceaccount.com
```

### 必要な権限

サービスアカウントには以下のロールが必要です：

- `roles/dataplex.viewer` - Dataplexリソースの読み取り
- `roles/dataplex.metadataReader` - メタデータアクセス
- `roles/dataplex.dataReader` - データ系譜情報アクセス

## 🛠️ 開発

### ローカル開発環境

```bash
# Poetry環境セットアップ
poetry install

# FastAPIサーバー起動
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### テスト実行

```bash
# 全テスト実行
poetry run pytest

# カバレッジ付き実行
poetry run pytest --cov=app --cov-report=html
```

### コード品質チェック

```bash
# Ruff による linting
poetry run ruff check .

# フォーマッティング
poetry run ruff format .
```

## ⚙️ 設定

### 環境変数

| 変数名 | 説明 | デフォルト値 |
|--------|------|-------------|
| `GOOGLE_CLOUD_PROJECT` | GCPプロジェクトID | `your-project-id` |
| `GOOGLE_CLOUD_LOCATION` | Dataplexロケーション | `us-central1` |
| `MCP_SERVER_NAME` | MCPサーバー名 | `dg-dataplex-mcp-server` |
| `LOG_LEVEL` | ログレベル | `INFO` |
| `PORT` | サーバーポート | `8080` |

## 🔒 セキュリティ

### 認証・認可

- **Identity Token認証**: Cloud Run間の認証にIdentity Tokenを使用
- **IAMベースアクセス制御**: 最小権限の原則に従ったロール設定
- **非rootユーザー実行**: セキュリティベストプラクティス準拠

### データ保護

- **機密情報管理**: 環境変数による適切な設定管理
- **詳細監査ログ**: 全ての操作とアクセスの記録
- **エラーハンドリング**: セキュアなエラー情報の提供

## 📊 技術スタック

- **Python 3.12+**
- **FastAPI** - 高性能WebAPIフレームワーク
- **Poetry 2.1.1** - 依存関係管理（バージョン固定）
- **Pydantic** - データバリデーション
- **Google Cloud Platform**
  - Cloud Run
  - Dataplex API
  - Identity & Access Management (IAM)

## 🔗 関連サービス

- **dg-dataplex-ai-agent**: Dataplex専門AIエージェント（このMCPサーバーを使用）
- **dg-data-governance-agent**: 親エージェント（間接連携）

詳細な開発ルールは [AGENTS.md](../../AGENTS.md) を参照してください。
