# Data Governance AI Agent System

## 🎯 提出作品

- [第3回 AI Agent Hackathon with Google Cloud](https://zenn.dev/hackathons/google-cloud-japan-ai-hackathon-vol3?tab=overview)
- Google Cloud上で動作するマルチエージェント構成のデータガバナンスシステムです。
- BigQueryテーブル(view)のメタデータやデータプロファイルの取得、データ品質ルールの提案を行うAIエージェントを提供します。

## 🏗️ システム構成

### マルチエージェント アーキテクチャ
- **親エージェント**: 統合的なデータガバナンス分析とエージェント間の調整
- **BigQuery AIエージェント**: BigQueryのメタデータ管理、リネージ・データプロファイルの取得
- **Dataplex AIエージェント**: Dataplexによるデータ品質ルール提案
- **MCPサーバー**: BigQuery/Dataplex APIとのインターフェース
- **Chat UI**: Chainlitベースのユーザーインターフェース

### 主要機能
- 📊 **データセット・テーブル分析**: メタデータ不足の自動検出
- 🏷️ **論理名・説明提案**: AIによる適切なメタデータ生成
- 🔗 **データリネージ分析**: テーブル間の依存関係可視化
- 🛡️ **データ品質ルール提案**: 統計情報に基づく品質チェック設定
- 📈 **ガバナンススコア算出**: 総合的なデータ品質評価
- 🤖 **マルチエージェント連携**: 複数の専門AIエージェントによる協調分析

### 🚀 技術スタック
- **MCP (Model Context Protocol)**: 最新のAIエージェント統合プロトコル
- **A2A (Agent-to-Agent)**: エージェント間の自律的な協調処理
- **Google ADK**: 独自AIエージェント(BigQuery/Dataplex)
- **Gemini 1.5 Flash**: Google最新LLMによる高速データ分析
- **Cloud Run**: サーバーレスでのスケーラブルなマイクロサービス構成
- **BigQuery**: メタデータとリネージの動的分析
- **Chainlit**: リアルタイムストリーミング対応のモダンChat UI

## 📁 プロジェクト構造

```
├── cloud_run/                    # Cloud Runサービス群
│   ├── dg-data-governance-agent/  # 親エージェント
│   ├── dg-bigquery-ai-agent/      # BigQuery専用エージェント
│   ├── dg-dataplex-ai-agent/      # Dataplex専用エージェント
│   ├── dg-bigquery-mcp-server/    # BigQuery MCPサーバー
│   ├── dg-dataplex-mcp-server/    # Dataplex MCPサーバー
│   └── dg-data-governance-chatui/ # Chainlit Chat UI
└── bigquery/                     # テストデータ・スキーマ
    ├── test_governance_tables.sql # サンプルテーブル定義
    └── README.md                  # テストデータ説明
```

## 🚀 クイックスタート

### 前提条件
- Google Cloud Platform アカウント
- BigQuery, Dataplex, Cloud Run の有効化
- Python 3.12+

### デプロイ手順
1. 各サービスディレクトリで `./deploy.sh <PROJECT_ID> <SERVICE_ACCOUNT>` を実行
2. 環境変数を設定してサービス間連携を構成
3. Chat UIからデータガバナンス分析を開始

詳細な手順は各サービスのREADMEを参照してください。

## ⚠️ 重要な注意事項

### FIXMEコメントについて
本プロジェクトには `# FIXME: プロジェクトIDを適宜変更` というコメントが含まれています。
**実際にデプロイする際は、これらの箇所を必ず実際のプロジェクトIDに変更してください。**

主な修正箇所：
- `cloud_run/*/app/core/config.py` - デフォルトプロジェクトID
- `cloud_run/*/app/services/*.py` - 各種サービスのデフォルト値

### テストデータについて
`bigquery/test_governance_tables.sql` にはサンプルテーブルが定義されており、デモ・検証用に使用できます。

### Cloud Runの設定値について
各AIエージェント並びに各MCPサーバーの最小インスタンス数を1としているため、サービスをデプロイするとインスタンスの維持費が発生します。
