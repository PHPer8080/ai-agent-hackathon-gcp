# DG BigQuery MCP Server

BigQuery専用MCPサーバー - データガバナンス機能

## 📋 概要

BigQuery MCP Serverは、BigQueryのデータガバナンス機能を提供するMCPサーバーです。dg-bigquery-ai-agentと連携し、BigQueryデータセット・テーブルの管理とガバナンス機能を提供します。

## 🏗️ アーキテクチャ

```text
dg-bigquery-ai-agent → dg-bigquery-mcp-server → BigQuery API
```

## 🔧 主要機能

- **データセット一覧取得**: BigQueryプロジェクト内のデータセット一覧を取得
- **テーブル詳細取得**: テーブル構造・メタデータの詳細分析
- **クエリ実行**: 安全なBigQueryクエリの実行
- **データガバナンス**: テーブル説明・ラベル不足の検出と優先度付け

## 🚀 デプロイ

```bash
./deploy.sh <PROJECT_ID> <SERVICE_ACCOUNT>

# 例
./deploy.sh your-project-id your-service-account@your-project-id.iam.gserviceaccount.com
```

## 📊 技術スタック

- **Python 3.12+**: プログラミング言語
- **FastAPI**: Webフレームワーク
- **fastapi-mcp**: MCP統合ライブラリ
- **google-cloud-bigquery**: BigQuery API クライアント
- **Poetry 2.1.1**: 依存関係管理（バージョン固定）
- **Pydantic**: データバリデーション

## 🔒 セキュリティ

### 認証・認可

- **Identity Token認証**: Cloud Run間の認証にIdentity Tokenを使用
- **IAMベースアクセス制御**: 最小権限の原則に従ったロール設定
- **非rootユーザー実行**: セキュリティベストプラクティス準拠

### データ保護

- **読み取り専用クエリ**: SELECT文のみ許可、変更系操作は禁止
- **機密情報管理**: 環境変数による適切な設定管理
- **詳細監査ログ**: 全ての操作とアクセスの記録

## 🔗 関連サービス

- **dg-bigquery-ai-agent**: BigQuery専用AIエージェント（このMCPサーバーを使用）
- **dg-data-governance-agent**: 親エージェント（間接連携）
