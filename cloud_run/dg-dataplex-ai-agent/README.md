# DG Dataplex AI Agent

Dataplex専用AIエージェントサービス

## 📋 概要

Google Cloud Dataplexの操作を自動化するAIエージェントのCloud Runサービスです。dg-data-governance-agentの子エージェントとして動作し、Dataplex関連の専門的なタスクを実行します。

## 🏗️ アーキテクチャ

```text
dg-data-governance-agent (親エージェント)
    ↓ A2A通信
dg-dataplex-ai-agent (子エージェント)
    ↓ MCP通信
dg-dataplex-mcp-server (MCPサーバー)
    ↓ API呼び出し
Google Cloud Dataplex API
```

## 🔧 主要機能

### MCPサーバー経由で提供

このエージェントは `dg-dataplex-mcp-server` を通じて以下の機能を提供します：

- **データアセット管理**: Dataplexアセットの一覧・詳細取得
- **データ系譜分析**: データフローと依存関係の可視化
- **データ品質監視**: 品質ルール・メトリクスの確認
- **メタデータ管理**: タグ付けとメタデータ整理
- **BigQueryメタデータ統合**: Dataplex API経由でのBigQueryメタデータ取得
- **🛡️ ガードレール機能**: セキュリティ・ポリシーチェック

## 🛡️ ガードレール機能

Google ADKの`before_tool_callback`を使用して、function calling前にセキュリティ・ポリシーチェックを実装しています。

### セキュリティガードレール

1. **危険なプロジェクト制限**: 本番環境プロジェクトへのアクセス拒否
2. **削除・変更系操作の制限**: 危険な操作の実行拒否
3. **機密データアクセス制御**: 機密情報を含む引数の拒否
4. **監査ログ記録**: 全ツール実行の詳細ログ記録

## 🚀 デプロイ

```bash
# Cloud Runにデプロイ
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
  - Dataplex API
  - Vertex AI

## 🔗 関連サービス

- **dg-data-governance-agent**: 親エージェント（このエージェントを呼び出し）
- **dg-dataplex-mcp-server**: Dataplex API統合サーバー（このエージェントが使用）
