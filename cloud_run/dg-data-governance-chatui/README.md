# 🏞️ Data Governance ChatUI

Google Cloud Dataplex・BigQueryを使ったデータガバナンス管理のためのChainlit WebUIです。

## 📋 概要

`dg-data-governance-agent`と連携し、直感的なチャットインターフェースでデータガバナンス業務を支援します。Dataplex・BigQuery両方のデータソースを統合分析できます。

## 🎯 主な機能

### Dataplex機能

- **データアセット管理**: Dataplexアセットの一覧・検索
- **データ系譜分析**: データフローと依存関係の可視化
- **データ品質監視**: 品質ルール・メトリクス確認
- **メタデータ管理**: タグ付けとメタデータ整理

### BigQuery機能

- **データセット管理**: BigQueryデータセット・テーブル一覧
- **テーブル分析**: テーブル構造・メタデータ詳細確認
- **クエリ実行**: 安全なBigQueryクエリ実行
- **ガバナンス確認**: 説明・ラベル不足テーブルの検出

### 統合機能

- **包括的分析**: Dataplex・BigQuery横断での統合分析
- **ガバナンス提案**: データ管理改善のための具体的アドバイス

## 🏗️ アーキテクチャ

```text
[User] → [ChatUI (Chainlit)] → [dg-data-governance-agent] →
    ├── [dg-dataplex-ai-agent] → [Dataplex API]
    └── [dg-bigquery-ai-agent] → [BigQuery API]
```

## 🚀 デプロイ方法

### 前提条件

- `dg-data-governance-agent`がデプロイ済み
- `dg-dataplex-ai-agent`がデプロイ済み
- `dg-bigquery-ai-agent`がデプロイ済み
- 適切なGCPプロジェクトとサービスアカウント権限

### デプロイコマンド

```bash
cd cloud_run/dg-data-governance-chatui
./deploy.sh <PROJECT_ID> <SERVICE_ACCOUNT>

# 例
./deploy.sh your-project-id sample-service-account@your-project-id.iam.gserviceaccount.com
```

## 🔧 環境変数

### AGENT_URL

- **説明**: データガバナンスエージェントのURL
- **デフォルト**: `https://dg-data-governance-agent-{PROJECT_ID}.asia-northeast1.run.app`

### PORT

- **説明**: Chainlitサーバーポート
- **デフォルト**: `8000`

## 📱 UI 機能

### プリセットプロンプト

#### Dataplexプリセット

- 🏞️ **データアセット一覧**: Dataplexアセットの表示
- 🔗 **データ系譜分析**: 依存関係の可視化
- 📊 **データ品質確認**: 品質メトリクス取得

#### BigQueryプリセット

- 🗃️ **データセット一覧**: BigQueryデータセット表示
- 📋 **テーブル詳細**: テーブル構造・メタデータ確認
- 🔍 **クエリ実行**: 安全なSQLクエリ実行

#### 統合分析プリセット

- 🛡️ **ガバナンス状況分析**: 包括的な現状評価
- 🏷️ **メタデータタグ管理**: タグ情報の整理
- 💡 **改善提案**: 具体的なアクションアイテム

### レスポンス表示

- **🏞️ Dataplex分析結果**: Dataplex専門エージェントからの詳細データ
- **🗃️ BigQuery分析結果**: BigQuery専門エージェントからの詳細データ
- **🛡️ データガバナンス観点**: 親エージェントからの統合分析・提案

## 🔒 セキュリティ

- **認証**: Cloud Run Identity Tokenによる認証
- **非rootユーザー実行**: セキュリティベストプラクティス準拠
- **Cloud Run統合**: マネージドサービスのセキュリティ機能活用

## 🧪 ローカル開発

```bash
# Poetry環境セットアップ
poetry install

# 環境変数設定
export AGENT_URL="https://dg-data-governance-agent-your-project.asia-northeast1.run.app"

# Chainlitアプリ起動
poetry run chainlit run app.py
```

## 📊 技術スタック

- **フレームワーク**: Chainlit 1.2.0
- **言語**: Python 3.12
- **HTTP通信**: aiohttp（非同期）
- **認証**: Google Cloud Identity Token
- **デプロイ**: Cloud Run
- **依存関係管理**: Poetry

## 🔗 関連サービス

- `dg-data-governance-agent`: 親エージェント（このUIが接続）
- `dg-dataplex-ai-agent`: Dataplex専門子エージェント
- `dg-bigquery-ai-agent`: BigQuery専門子エージェント

## 📝 使用例

### 基本的な質問

#### Dataplex操作

```text
「Dataplexのデータアセットを一覧表示して」
「データ品質ルールの実行結果を確認して」
```

#### BigQuery操作

```text
「BigQueryのtt_hackathonデータセットのテーブル一覧を表示して」
「説明が設定されていないテーブルを検出して」
```

### 高度な統合分析

```text
「BigQueryのtt_hackathonとDataplexアセットの品質状況を統合分析して」
「プロジェクト全体のデータガバナンス状況を分析して」
「メタデータタグの整理状況と改善提案をお願いします」
```

## 🛠️ トラブルシューティング

### 接続エラー

- `AGENT_URL`環境変数を確認
- `dg-data-governance-agent`の動作状況を確認

### 認証エラー

- サービスアカウント権限を確認
- Cloud Runサービス間の通信設定を確認

### タイムアウト

- 複雑なクエリはタイムアウト（120秒）の可能性
- 処理時間の長い分析は分割して実行

---

最終更新: 2025-09-15
