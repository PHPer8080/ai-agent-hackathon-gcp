-- データガバナンステスト用テーブル作成スクリプト
-- 各種パターンを網羅した10テーブルを作成

-- =============================================================================
-- 1. raw_customers (上流のみ・説明なし・論理名なし・データあり)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_us.raw_customers` (
  customer_id STRING,
  first_name STRING,
  last_name STRING,
  email STRING,
  phone STRING,
  created_at TIMESTAMP
)
OPTIONS(
  -- 意図的に説明を設定しない
  -- 意図的にラベル（論理名）を設定しない
);

-- サンプルデータ挿入
INSERT INTO `tt_us.raw_customers` VALUES
  ('CUST001', 'John', 'Doe', 'john.doe@example.com', '090-1234-5678', CURRENT_TIMESTAMP()),
  ('CUST002', 'Jane', 'Smith', 'jane.smith@example.com', '090-2345-6789', CURRENT_TIMESTAMP()),
  ('CUST003', 'Mike', 'Johnson', 'mike.johnson@example.com', '090-3456-7890', CURRENT_TIMESTAMP());

-- =============================================================================
-- 2. raw_products (上流のみ・説明なし・論理名あり・データあり)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_us.raw_products` (
  product_id STRING,
  product_name STRING,
  category STRING,
  price NUMERIC,
  stock_quantity INT64,
  created_at TIMESTAMP
)
OPTIONS(
  -- 意図的に説明を設定しない
  labels=[
    ("logical_name", "product_master_data"),
    ("data_source", "external_api"),
    ("update_frequency", "daily")
  ]
);

-- サンプルデータ挿入
INSERT INTO `tt_us.raw_products` VALUES
  ('PROD001', 'ノートパソコン', 'Electronics', 89800, 50, CURRENT_TIMESTAMP()),
  ('PROD002', 'マウス', 'Electronics', 2980, 200, CURRENT_TIMESTAMP()),
  ('PROD003', 'キーボード', 'Electronics', 5980, 100, CURRENT_TIMESTAMP());

-- =============================================================================
-- 3. raw_orders (上流のみ・説明あり・論理名なし・データNULL)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_us.raw_orders` (
  order_id STRING,
  customer_id STRING,
  order_date TIMESTAMP,
  total_amount NUMERIC,
  status STRING,
  notes STRING
)
OPTIONS(
  description="生の注文データ。外部システムから取得した未加工の注文情報を格納。データ品質に問題がある可能性があります。"
  -- 意図的にラベル（論理名）を設定しない
);

-- NULLデータを含むサンプルデータ挿入
INSERT INTO `tt_us.raw_orders` VALUES
  ('ORD001', 'CUST001', CURRENT_TIMESTAMP(), 92780, 'completed', 'Normal order'),
  ('ORD002', NULL, CURRENT_TIMESTAMP(), NULL, 'pending', NULL),  -- NULLデータ
  ('ORD003', 'CUST003', NULL, 5980, NULL, 'Incomplete data');   -- NULLデータ

-- =============================================================================
-- 4. customer_profiles (上流・下流両方・説明あり・論理名あり・データあり)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_us.customer_profiles` (
  profile_id STRING,
  customer_id STRING,
  full_name STRING,
  email_verified BOOL,
  total_orders INT64,
  total_spent NUMERIC,
  customer_segment STRING,
  last_activity TIMESTAMP,
  created_at TIMESTAMP
)
OPTIONS(
  description="顧客プロファイル情報。raw_customersから加工された顧客の詳細情報と購買履歴を含む統合データ。",
  labels=[
    ("logical_name", "customer_profile_integrated_table"),
    ("data_quality", "high"),
    ("business_critical", "true"),
    ("pii_data", "true")
  ]
);

-- 依存関係を示すためのビュー作成（上流依存）
CREATE OR REPLACE VIEW `tt_us.customer_profiles_source` AS
SELECT
  CONCAT('PROF_', customer_id) as profile_id,
  customer_id,
  CONCAT(first_name, ' ', last_name) as full_name,
  CASE WHEN email IS NOT NULL THEN true ELSE false END as email_verified,
  0 as total_orders,
  CAST(0.0 AS NUMERIC) as total_spent,
  'new' as customer_segment,
  created_at as last_activity,
  created_at
FROM `tt_us.raw_customers`;

-- サンプルデータ挿入
INSERT INTO `tt_us.customer_profiles`
SELECT * FROM `tt_us.customer_profiles_source`;

-- =============================================================================
-- 5. product_catalog (上流・下流両方・説明なし・論理名なし・データNULL)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_us.product_catalog` (
  catalog_id STRING,
  product_id STRING,
  display_name STRING,
  description STRING,
  category_path STRING,
  price_tier STRING,
  availability_status STRING,
  last_updated TIMESTAMP
)
OPTIONS(
  -- 意図的に説明を設定しない
  -- 意図的にラベル（論理名）を設定しない
);

-- NULLデータを含むサンプルデータ挿入
INSERT INTO `tt_us.product_catalog` VALUES
  ('CAT001', 'PROD001', 'ノートパソコン', NULL, 'Electronics/Computers', 'premium', 'available', CURRENT_TIMESTAMP()),
  ('CAT002', NULL, NULL, NULL, NULL, NULL, NULL, NULL),  -- 全てNULL
  ('CAT003', 'PROD003', 'キーボード', 'Mechanical keyboard', NULL, 'standard', NULL, CURRENT_TIMESTAMP());

-- =============================================================================
-- 6. order_details (上流・下流両方・説明あり・論理名なし・データあり)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_us.order_details` (
  detail_id STRING,
  order_id STRING,
  customer_id STRING,
  order_date TIMESTAMP,
  total_amount NUMERIC,
  payment_method STRING,
  shipping_address STRING,
  processed_at TIMESTAMP
)
OPTIONS(
  description="注文詳細情報。raw_ordersから加工された注文の詳細データ。支払い方法や配送先情報を含む。"
  -- 意図的にラベル（論理名）を設定しない
);

-- サンプルデータ挿入
INSERT INTO `tt_us.order_details` VALUES
  ('DTL001', 'ORD001', 'CUST001', CURRENT_TIMESTAMP(), 92780, 'credit_card', '東京都渋谷区1-1-1', CURRENT_TIMESTAMP()),
  ('DTL002', 'ORD003', 'CUST003', CURRENT_TIMESTAMP(), 5980, 'bank_transfer', '大阪府大阪市2-2-2', CURRENT_TIMESTAMP());

-- =============================================================================
-- 7. order_items (上流・下流両方・説明なし・論理名あり・データあり)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_us.order_items` (
  item_id STRING,
  order_id STRING,
  product_id STRING,
  quantity INT64,
  unit_price NUMERIC,
  total_price NUMERIC,
  discount_amount NUMERIC,
  created_at TIMESTAMP
)
OPTIONS(
  -- 意図的に説明を設定しない
  labels=[
    ("logical_name", "order_item_detail_table"),
    ("granularity", "item_level"),
    ("calculation_base", "true")
  ]
);

-- サンプルデータ挿入
INSERT INTO `tt_us.order_items` VALUES
  ('ITEM001', 'ORD001', 'PROD001', 1, 89800, 89800, 0, CURRENT_TIMESTAMP()),
  ('ITEM002', 'ORD001', 'PROD002', 1, 2980, 2980, 0, CURRENT_TIMESTAMP()),
  ('ITEM003', 'ORD003', 'PROD003', 1, 5980, 5980, 0, CURRENT_TIMESTAMP());

-- =============================================================================
-- 8. customer_analytics (下流のみ・説明あり・論理名あり・データNULL)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_us.customer_analytics` (
  analytics_id STRING,
  customer_id STRING,
  total_lifetime_value NUMERIC,
  average_order_value NUMERIC,
  order_frequency NUMERIC,
  churn_probability NUMERIC,
  customer_score INT64,
  last_calculated TIMESTAMP
)
OPTIONS(
  description="顧客分析データ。customer_profilesから算出された顧客の行動分析と予測データ。機械学習モデルの結果を含む。",
  labels=[
    ("logical_name", "customer_behavior_analytics_table"),
    ("data_type", "analytics"),
    ("ml_generated", "true"),
    ("business_value", "high")
  ]
);

-- NULLデータを含むサンプルデータ挿入
INSERT INTO `tt_us.customer_analytics` VALUES
  ('ANAL001', 'CUST001', 92780, 92780, 1.0, 0.2, 85, CURRENT_TIMESTAMP()),
  ('ANAL002', 'CUST002', NULL, NULL, NULL, NULL, NULL, NULL),  -- 全てNULL（計算失敗）
  ('ANAL003', 'CUST003', 5980, 5980, NULL, 0.8, 45, CURRENT_TIMESTAMP());

-- =============================================================================
-- 9. sales_summary (下流のみ・説明なし・論理名なし・データあり)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_us.sales_summary` (
  summary_id STRING,
  summary_date DATE,
  total_orders INT64,
  total_revenue NUMERIC,
  average_order_value NUMERIC,
  top_product_category STRING,
  customer_count INT64,
  created_at TIMESTAMP
)
OPTIONS(
  -- 意図的に説明を設定しない
  -- 意図的にラベル（論理名）を設定しない
);

-- サンプルデータ挿入
INSERT INTO `tt_us.sales_summary` VALUES
  ('SUM001', CURRENT_DATE(), 2, 98760, 49380, 'Electronics', 2, CURRENT_TIMESTAMP()),
  ('SUM002', DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY), 1, 5980, 5980, 'Electronics', 1, CURRENT_TIMESTAMP());

-- =============================================================================
-- 10. monthly_reports (下流のみ・説明あり・論理名なし・データあり)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_us.monthly_reports` (
  report_id STRING,
  report_month STRING,
  total_customers INT64,
  new_customers INT64,
  total_orders INT64,
  total_revenue NUMERIC,
  top_products ARRAY<STRING>,
  kpi_metrics JSON,
  generated_at TIMESTAMP
)
OPTIONS(
  description="月次レポートデータ。sales_summaryやcustomer_analyticsから集計された月次の業績データ。経営陣向けのKPI情報を含む。"
  -- 意図的にラベル（論理名）を設定しない
);

-- サンプルデータ挿入
INSERT INTO `tt_us.monthly_reports` VALUES
  ('RPT001', '2025-09', 3, 3, 2, 98760, ['PROD001', 'PROD003'], JSON '{"conversion_rate": 0.67, "customer_satisfaction": 4.2}', CURRENT_TIMESTAMP());

-- =============================================================================
-- 依存関係を明確にするためのビュー作成
-- =============================================================================

-- customer_analytics ← customer_profiles の依存関係
CREATE OR REPLACE VIEW `tt_us.customer_analytics_base` AS
SELECT
  CONCAT('ANAL_', customer_id) as analytics_id,
  customer_id,
  total_spent as total_lifetime_value,
  CASE WHEN total_orders > 0 THEN total_spent / total_orders ELSE CAST(0 AS NUMERIC) END as average_order_value,
  CAST(total_orders AS NUMERIC) / 30.0 as order_frequency,
  CASE WHEN total_orders = 0 THEN 0.9 ELSE 0.1 END as churn_probability,
  CASE
    WHEN total_spent > 50000 THEN 90
    WHEN total_spent > 10000 THEN 70
    ELSE 50
  END as customer_score,
  CURRENT_TIMESTAMP() as last_calculated
FROM `tt_us.customer_profiles`;

-- sales_summary ← order_details, order_items の依存関係
CREATE OR REPLACE VIEW `tt_us.sales_summary_base` AS
SELECT
  CONCAT('SUM_', FORMAT_DATE('%Y%m%d', summary_date)) as summary_id,
  summary_date,
  total_orders,
  total_revenue,
  average_order_value,
  'Electronics' as top_product_category,
  customer_count,
  CURRENT_TIMESTAMP() as created_at
FROM (
  SELECT
    DATE(od.order_date) as summary_date,
    COUNT(DISTINCT od.order_id) as total_orders,
    SUM(od.total_amount) as total_revenue,
    AVG(od.total_amount) as average_order_value,
    COUNT(DISTINCT od.customer_id) as customer_count
  FROM `tt_us.order_details` od
  GROUP BY DATE(od.order_date)
);

-- monthly_reports ← sales_summary, customer_analytics の依存関係
CREATE OR REPLACE VIEW `tt_us.monthly_reports_base` AS
SELECT
  CONCAT('RPT_', FORMAT_DATE('%Y%m', CURRENT_DATE())) as report_id,
  FORMAT_DATE('%Y-%m', CURRENT_DATE()) as report_month,
  (SELECT COUNT(*) FROM `tt_us.customer_profiles`) as total_customers,
  (SELECT COUNT(*) FROM `tt_us.customer_profiles`) as new_customers,
  (SELECT SUM(total_orders) FROM `tt_us.sales_summary`) as total_orders,
  (SELECT SUM(total_revenue) FROM `tt_us.sales_summary`) as total_revenue,
  ['PROD001', 'PROD002', 'PROD003'] as top_products,
  JSON '{"conversion_rate": 0.75, "customer_satisfaction": 4.5}' as kpi_metrics,
  CURRENT_TIMESTAMP() as generated_at;
