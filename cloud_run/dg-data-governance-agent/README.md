# DG Data Governance Agent

A2Aマルチエージェント構成の親エージェント（データガバナンス戦略立案・調整）

## 📋 概要

データガバナンス全体の戦略立案と子エージェントの調整を行う親エージェントです。専門的なタスクは適切な子エージェントに委譲し、結果を統合して包括的な回答を提供します。

## 🏗️ アーキテクチャ

```text
dg-data-governance-agent (親エージェント)
    ├── dg-dataplex-ai-agent (Dataplex専門)
    │   └── dg-dataplex-mcp-server
    └── dg-bigquery-ai-agent (BigQuery専門)
        └── dg-bigquery-mcp-server
```

## 🚀 機能

### 親エージェント機能

- **データガバナンス戦略立案**: 包括的なガバナンス方針の提案
- **子エージェント調整**: Dataplex・BigQuery専門エージェントとの連携
- **統合分析**: 複数データソースからの結果統合
- **ガバナンス推奨事項**: 実践的な改善提案

### A2A連携機能

- **Dataplex連携**: データアセット・品質・系譜分析
- **BigQuery連携**: データセット・テーブル・クエリ分析
- **非同期通信**: 子エージェントとの効率的な通信
- **結果統合処理**: 複数の分析結果を統合した回答生成

## 📡 API エンドポイント

### POST /chat

AIエージェントとのチャットエンドポイント

**リクエスト:**

```json
{
  "message": "BigQueryのtt_hackathonデータセットとDataplexの品質状況を教えて",
  "session_id": "optional-session-id"
}
```

**レスポンス:**

```json
{
  "response": "BigQueryとDataplexの統合分析結果...",
  "session_id": "session-id",
  "delegated_agents": ["dg-bigquery-ai-agent", "dg-dataplex-ai-agent"]
}
```

### GET /health

ヘルスチェックエンドポイント

## 🔧 設定

### 環境変数

| 変数名 | 説明 | 必須 |
|--------|------|------|
| `DG_DATAPLEX_AI_AGENT_URL` | Dataplex AIエージェントのURL | Yes |
| `DG_BIGQUERY_AI_AGENT_URL` | BigQuery AIエージェントのURL | Yes |

## 🚀 デプロイ

```bash
# デプロイ実行
./deploy.sh <PROJECT_ID> <SERVICE_ACCOUNT>

# 例
./deploy.sh your-project-id sample-service-account@your-project-id.iam.gserviceaccount.com
```

## 🔍 使用例

### 統合データガバナンス分析

```bash
curl -X POST "https://dg-data-governance-agent-xxx.run.app/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "tt_hackathonのBigQueryテーブルとDataplexアセットの品質状況を統合分析して"
  }'
```

### BigQuery専門分析

```bash
curl -X POST "https://dg-data-governance-agent-xxx.run.app/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "BigQueryのtt_hackathonデータセットのテーブル一覧と説明不足を確認して"
  }'
```

### Dataplex専門分析

```bash
curl -X POST "https://dg-data-governance-agent-xxx.run.app/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Dataplexのデータアセット一覧と品質ルール実行状況を教えて"
  }'
```

## 🔗 関連サービス

| サービス | 説明 | 関係 |
|----------|------|------|
| `dg-dataplex-ai-agent` | Dataplex専門エージェント | 子エージェント |
| `dg-bigquery-ai-agent` | BigQuery専門エージェント | 子エージェント |
| `dg-data-governance-chatui` | WebUI | このエージェントを使用 |

## 🛠️ 開発

### ローカル起動

```bash
# 依存関係インストール
poetry install

# 環境変数設定
export DG_DATAPLEX_AI_AGENT_URL="https://dg-dataplex-ai-agent-xxx.run.app"
export DG_BIGQUERY_AI_AGENT_URL="https://dg-bigquery-ai-agent-xxx.run.app"

# 開発サーバー起動
poetry run uvicorn app.main:app --reload --port 8000
```

### テスト

```bash
# テスト実行
poetry run pytest
```

## 📝 ログ・監視

- Google Cloud Logging統合
- 構造化ログ出力
- 子エージェント委譲の詳細ログ
- パフォーマンス監視

---

最終更新: 2025-09-15
