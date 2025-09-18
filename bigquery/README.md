# BigQuery tt_hackathon Dataset

データガバナンステスト用データセット（ハッカソン用）

## 📊 テストパターン

### 主要テーブル一覧（60テーブル中の代表例）

| # | テーブル名 | 説明 | 論理名 | データ | 依存関係 | テスト目的 |
|---|-----------|------|--------|--------|----------|-----------|
| 1 | **raw_customers** | ❌なし | ❌なし | ✅あり | 上流のみ | 説明・論理名不足 |
| 2 | **raw_products** | ❌なし | ✅あり | ✅あり | 上流のみ | 説明不足のみ |
| 3 | **raw_orders** | ✅あり | ❌なし | ❌NULL含む | 上流のみ | 論理名不足・NULLデータ |
| 4 | **customer_profiles** | ✅あり | ✅あり | ✅あり | 上流・下流両方 | 完全なメタデータ |
| 5 | **product_catalog** | ❌なし | ❌なし | ❌NULL含む | 上流・下流両方 | 全て不足・NULLデータ |
| 6 | **order_details** | ✅あり | ❌なし | ✅あり | 上流・下流両方 | 論理名のみ不足 |
| 7 | **order_items** | ❌なし | ✅あり | ✅あり | 上流・下流両方 | 説明のみ不足 |
| 8 | **customer_analytics** | ✅あり | ✅あり | ❌NULL含む | 下流のみ | 完全だがNULLデータ |
| 9 | **sales_summary** | ❌なし | ❌なし | ✅あり | 下流のみ | 説明・論理名不足 |
| 10 | **monthly_reports** | ✅あり | ❌なし | ✅あり | 下流のみ | 論理名のみ不足 |

### テストパターン分類

#### 📋 メタデータ不足パターン

- **説明なし**: `raw_customers`, `raw_products`, `product_catalog`, `order_items`, `sales_summary`
- **論理名なし**: `raw_customers`, `raw_orders`, `product_catalog`,
  `order_details`, `sales_summary`, `monthly_reports`
- **両方なし**: `raw_customers`, `product_catalog`, `sales_summary`

#### 💾 データ品質パターン

- **正常データ**: `raw_customers`, `raw_products`, `customer_profiles`,
  `order_details`, `order_items`, `sales_summary`, `monthly_reports`
- **NULLデータ含む**: `raw_orders`, `product_catalog`, `customer_analytics`

#### 🔗 依存関係パターン

- **上流のみ（ソース）**: `raw_customers`, `raw_products`, `raw_orders`
- **上流・下流両方（中間）**: `customer_profiles`, `product_catalog`, `order_details`, `order_items`
- **下流のみ（シンク）**: `customer_analytics`, `sales_summary`, `monthly_reports`

## 🔗 データフロー構造

```text
📊 データリネージ構造（60テーブル中の主要フロー）:

上流テーブル（ソース）:
├── raw_customers → customer_profiles → customer_analytics
├── raw_products → product_catalog → sales_summary
├── raw_orders → order_details → monthly_reports
│               └── order_items → sales_summary
├── user_sessions → website_analytics → ab_test_results
├── inventory_movements → inventory_forecasts
├── payment_transactions → financial_transactions
└── employee_records → training_records

依存関係の詳細（コア業務フロー）:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  raw_customers  │───▶│customer_profiles│───▶│customer_analytics│
│  (上流のみ)      │    │  (上流・下流)    │    │  (下流のみ)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  raw_products   │───▶│ product_catalog │───▶│  sales_summary  │
│  (上流のみ)      │    │  (上流・下流)    │    │  (下流のみ)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘

追加フロー（分析・監視系）:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  user_sessions  │───▶│website_analytics│───▶│ ab_test_results │
└─────────────────┘    └─────────────────┘    └─────────────────┘

┌─────────────────┐    ┌─────────────────┐
│inventory_movements│───▶│inventory_forecasts│
└─────────────────┘    └─────────────────┘
```

### 依存関係パターン分類

#### 🔵 上流のみ（ソーステーブル）

**コア業務データ:**

- `raw_customers` - 顧客の生データ
- `raw_products` - 商品の生データ
- `raw_orders` - 注文の生データ

**運用・監視データ:**

- `user_sessions` - ユーザーセッション情報
- `inventory_movements` - 在庫移動履歴
- `payment_transactions` - 決済取引履歴
- `employee_records` - 従業員記録
- `audit_logs` - 監査ログ
- `security_events` - セキュリティイベント

#### 🟡 上流・下流両方（中間テーブル）

**業務処理データ:**

- `customer_profiles` - 顧客プロファイル統合データ
- `product_catalog` - 商品カタログデータ
- `order_details` - 注文詳細データ
- `order_items` - 注文商品明細データ

**分析・監視データ:**

- `website_analytics` - ウェブサイト分析データ
- `performance_metrics` - パフォーマンス指標
- `integration_logs` - 統合ログ

#### 🔴 下流のみ（シンクテーブル）

**分析結果:**

- `customer_analytics` - 顧客分析結果
- `sales_summary` - 売上サマリー
- `monthly_reports` - 月次レポート
- `inventory_forecasts` - 在庫需要予測
- `ab_test_results` - A/Bテスト結果

**機械学習・AI:**

- `ml_model_predictions` - 機械学習予測結果
- `price_optimization_data` - 価格最適化データ

## 🧪 テスト可能な機能（60テーブル対応）

### BigQuery AI Agent テスト

**メタデータ管理:**

- ✅ 説明不足テーブルの検出（約25テーブル）
- ✅ 論理名不足テーブルの検出（約20テーブル）
- ✅ 論理名・説明の提案
- ✅ カラム説明の確認

**データ品質分析:**

- ✅ 統計情報取得・分析
- ✅ NULLデータ検出
- ✅ データ型整合性チェック
- ✅ ガバナンススコア計算

### Dataplex AI Agent テスト

**データリネージ:**

- ✅ データリネージの取得（60テーブル対応）
- ✅ 上流依存関係の分析
- ✅ 下流依存関係の分析
- ✅ データフローの可視化

**品質管理:**

- ✅ データ品質ルール提案
- ✅ 統計情報に基づく品質評価
- ✅ 異常データ検出

### Data Governance Agent テスト

**統合分析:**

- ✅ 統合テーブル説明の作成
- ✅ 複数エージェント連携（BigQuery + Dataplex）
- ✅ 包括的データガバナンス分析
- ✅ 60テーブル規模での性能テスト

**高度な機能:**

- ✅ セクター別データ分析（業務・運用・分析・AI）
- ✅ 大規模データセットでのガバナンス評価
- ✅ リアルタイム品質監視シミュレーション

## 📁 ファイル構成

```text
tt_hackathon/ (→ tt_hackathon用に更新)
├── README.md                    # このファイル
├── test_governance_tables.sql   # 60テーブル作成スクリプト（各1000件データ）
├── rag_document_ai.sql         # Document AI関連テーブル
├── rag_master.sql              # RAGマスターテーブル
└── rag_wagahai_sample.sql      # RAGサンプルテーブル
```

## 🚀 使用方法

### テーブル作成（60テーブル + 60,000件データ）

```bash
bq query --use_legacy_sql=false < bigquery/tt_hackathon/test_governance_tables.sql
```

### テーブル確認

```bash
# データセット内のテーブル一覧（60テーブル）
bq ls tt_hackathon

# テーブル数確認
bq ls tt_hackathon | wc -l
```

### 特定テーブルの詳細確認

```bash
# テーブル構造とメタデータ確認
bq show --format=prettyjson tt_hackathon.テーブル名

# データ件数確認（各テーブル1000件）
bq query --use_legacy_sql=false "SELECT COUNT(*) FROM tt_hackathon.テーブル名"
```

### データガバナンステスト例

```bash
# メタデータ不足テーブル検出
bq query --use_legacy_sql=false "
SELECT table_name, description
FROM tt_hackathon.INFORMATION_SCHEMA.TABLES
WHERE description IS NULL"

# 統計情報取得
bq query --use_legacy_sql=false "
SELECT * FROM tt_hackathon.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS
WHERE table_name = 'customer_profiles'"
```
