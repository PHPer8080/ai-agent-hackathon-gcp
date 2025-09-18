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

## 🔧 主要機能

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

## 🚀 デプロイ

```bash
# デプロイ実行
./deploy.sh <PROJECT_ID> <SERVICE_ACCOUNT>

# 例
./deploy.sh your-project-id your-service-account@your-project-id.iam.gserviceaccount.com
```

## 🔍 使用例

### 統合データガバナンス分析

```bash
curl -X POST "https://dg-data-governance-agent-xxx.run.app/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "tt_dlkのBigQueryテーブルとDataplexアセットの品質状況を統合分析して"
  }'
```

### BigQuery専門分析

```bash
curl -X POST "https://dg-data-governance-agent-xxx.run.app/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "BigQueryのtt_usデータセットのテーブル一覧と説明不足を確認して"
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

## 📊 技術スタック

- **Python 3.12+**: プログラミング言語
- **Poetry 2.1.1**: 依存関係管理（バージョン固定）
- **Google ADK**: AIエージェント開発キット
- **FastAPI**: Webフレームワーク
- **Google Cloud Platform**:
  - Cloud Run
  - Vertex AI
  - Identity & Access Management (IAM)

## 🔗 関連サービス

- **dg-dataplex-ai-agent**: Dataplex専門エージェント（子エージェント）
- **dg-bigquery-ai-agent**: BigQuery専門エージェント（子エージェント）
- **dg-data-governance-chatui**: WebUI（このエージェントを使用）
