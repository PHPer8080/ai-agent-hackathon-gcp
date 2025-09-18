# DG Data Governance ChatUI

Google Cloud Dataplex・BigQueryを使ったデータガバナンス管理のためのChainlit WebUI

## 📋 概要

`dg-data-governance-agent`と連携し、直感的なチャットインターフェースでデータガバナンス業務を支援します。Dataplex・BigQuery両方のデータソースを統合分析できます。

## 🏗️ アーキテクチャ

```text
[User] → [ChatUI (Chainlit)] → [dg-data-governance-agent] →
    ├── [dg-dataplex-ai-agent] → [Dataplex API]
    └── [dg-bigquery-ai-agent] → [BigQuery API]
```

## 🔧 主要機能

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

## 📱 UI 機能

### プリセットプロンプト

#### BigQueryプリセット

- 📊 **データセット一覧**: BigQueryデータセット表示
- 🔗 **データ系譜分析**: テーブル依存関係の可視化
- 📈 **ガバナンススコア**: データ品質とメタデータの評価
- 🏷️ **メタデータ不足検出**: 説明や論理名が不足しているテーブルを検出
- 📋 **カラム情報確認**: テーブルのカラム情報と説明を確認
- 📊 **統計情報分析**: データ品質の詳細分析

#### Dataplexプリセット

- 🛡️ **品質ルール提案**: 統計情報に基づく品質管理ルール
- 💡 **メタデータ提案**: 不足している論理名と説明を提案

### レスポンス表示

- **🏞️ Dataplex分析結果**: Dataplex専門エージェントからの詳細データ
- **🗃️ BigQuery分析結果**: BigQuery専門エージェントからの詳細データ
- **🛡️ データガバナンス観点**: 親エージェントからの統合分析・提案

## 🚀 デプロイ

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
./deploy.sh your-project-id your-service-account@your-project-id.iam.gserviceaccount.com
```

## 📊 技術スタック

- **フレームワーク**: Chainlit 1.2.0
- **言語**: Python 3.12
- **HTTP通信**: aiohttp（非同期）
- **認証**: Google Cloud Identity Token
- **デプロイ**: Cloud Run
- **依存関係管理**: Poetry

## 🔒 セキュリティ

- **認証**: Cloud Run Identity Tokenによる認証
- **非rootユーザー実行**: セキュリティベストプラクティス準拠
- **Cloud Run統合**: マネージドサービスのセキュリティ機能活用

## 📝 使用例

### 基本的な質問

#### Dataplex操作

```text
「Dataplexのデータアセットを一覧表示して」
「データ品質ルールの実行結果を確認して」
```

#### BigQuery操作

```text
「BigQueryのtt_dlkデータセットのテーブル一覧を表示して」
「説明が設定されていないテーブルを検出して」
```

### 高度な統合分析

```text
「BigQueryのtt_dlkとDataplexアセットの品質状況を統合分析して」
「プロジェクト全体のデータガバナンス状況を分析して」
「メタデータタグの整理状況と改善提案をお願いします」
```

## 🔗 関連サービス

- **dg-data-governance-agent**: 親エージェント（このUIが接続）
- **dg-dataplex-ai-agent**: Dataplex専門子エージェント
- **dg-bigquery-ai-agent**: BigQuery専門子エージェント
