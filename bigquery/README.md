# BigQuery tt_us Dataset

データガバナンステスト用データセット

## 📊 テストパターン

### テーブル一覧（10テーブル）

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
📊 データリネージ構造:

上流テーブル（ソース）:
├── raw_customers → customer_profiles → customer_analytics
├── raw_products → product_catalog → sales_summary
└── raw_orders → order_details → monthly_reports
                └── order_items → sales_summary

依存関係の詳細:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  raw_customers  │───▶│customer_profiles│───▶│customer_analytics│
│  (上流のみ)      │    │  (上流・下流)    │    │  (下流のみ)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  raw_products   │───▶│ product_catalog │───▶│  sales_summary  │
│  (上流のみ)      │    │  (上流・下流)    │    │  (下流のみ)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                               ▲
┌─────────────────┐    ┌─────────────────┐    │
│   raw_orders    │───▶│  order_details  │───▶│
│  (上流のみ)      │    │  (上流・下流)    │    │
└─────────────────┘    └─────────────────┘    │
         │                       │             │
         │              ┌─────────────────┐    │
         └─────────────▶│   order_items   │───▶│
                        │  (上流・下流)    │    │
                        └─────────────────┘    │
                                               │
┌─────────────────┐                           │
│ monthly_reports │◀──────────────────────────┘
│  (下流のみ)      │
└─────────────────┘
```

### 依存関係パターン分類

#### 🔵 上流のみ（ソーステーブル）

- `raw_customers` - 顧客の生データ
- `raw_products` - 商品の生データ
- `raw_orders` - 注文の生データ

#### 🟡 上流・下流両方（中間テーブル）

- `customer_profiles` - 顧客プロファイル統合データ
- `product_catalog` - 商品カタログデータ
- `order_details` - 注文詳細データ
- `order_items` - 注文商品明細データ

#### 🔴 下流のみ（シンクテーブル）

- `customer_analytics` - 顧客分析結果
- `sales_summary` - 売上サマリー
- `monthly_reports` - 月次レポート

## 🧪 テスト可能な機能

### BigQuery AI Agent テスト

- ✅ 説明不足テーブルの検出
- ✅ 論理名不足テーブルの検出
- ✅ 論理名・説明の提案
- ✅ カラム説明の確認

### Dataplex AI Agent テスト

- ✅ データリネージの取得
- ✅ 上流依存関係の分析
- ✅ 下流依存関係の分析
- ✅ データフローの可視化

### Data Governance Agent テスト

- ✅ 統合テーブル説明の作成
- ✅ 複数エージェント連携
- ✅ 包括的データガバナンス分析
