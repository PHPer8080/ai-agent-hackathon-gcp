-- データガバナンステスト用テーブル作成スクリプト
-- 各種パターンを網羅した60テーブルを作成（既存10 + 新規50）
-- 各テーブルに1000件のダミーデータを挿入

-- =============================================================================
-- 1. raw_customers (上流のみ・説明なし・論理名なし・データあり)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.raw_customers` (
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

-- 1000件のダミーデータ挿入
INSERT INTO `tt_hackathon.raw_customers`
WITH dummy_data AS (
  SELECT
    CONCAT('CUST', LPAD(CAST(seq AS STRING), 6, '0')) as customer_id,
    CASE MOD(seq, 20)
      WHEN 0 THEN 'John' WHEN 1 THEN 'Jane' WHEN 2 THEN 'Mike' WHEN 3 THEN 'Sarah'
      WHEN 4 THEN 'David' WHEN 5 THEN 'Emily' WHEN 6 THEN 'Chris' WHEN 7 THEN 'Lisa'
      WHEN 8 THEN 'Mark' WHEN 9 THEN 'Anna' WHEN 10 THEN 'Tom' WHEN 11 THEN 'Kate'
      WHEN 12 THEN 'Paul' WHEN 13 THEN 'Amy' WHEN 14 THEN 'Steve' WHEN 15 THEN 'Emma'
      WHEN 16 THEN 'Alex' WHEN 17 THEN 'Grace' WHEN 18 THEN 'Ryan' ELSE 'Sophia'
    END as first_name,
    CASE MOD(seq, 15)
      WHEN 0 THEN 'Smith' WHEN 1 THEN 'Johnson' WHEN 2 THEN 'Williams' WHEN 3 THEN 'Brown'
      WHEN 4 THEN 'Jones' WHEN 5 THEN 'Garcia' WHEN 6 THEN 'Miller' WHEN 7 THEN 'Davis'
      WHEN 8 THEN 'Rodriguez' WHEN 9 THEN 'Martinez' WHEN 10 THEN 'Hernandez' WHEN 11 THEN 'Lopez'
      WHEN 12 THEN 'Gonzalez' WHEN 13 THEN 'Wilson' ELSE 'Anderson'
    END as last_name,
    CONCAT(
      CASE MOD(seq, 20)
        WHEN 0 THEN 'john' WHEN 1 THEN 'jane' WHEN 2 THEN 'mike' WHEN 3 THEN 'sarah'
        WHEN 4 THEN 'david' WHEN 5 THEN 'emily' WHEN 6 THEN 'chris' WHEN 7 THEN 'lisa'
        WHEN 8 THEN 'mark' WHEN 9 THEN 'anna' WHEN 10 THEN 'tom' WHEN 11 THEN 'kate'
        WHEN 12 THEN 'paul' WHEN 13 THEN 'amy' WHEN 14 THEN 'steve' WHEN 15 THEN 'emma'
        WHEN 16 THEN 'alex' WHEN 17 THEN 'grace' WHEN 18 THEN 'ryan' ELSE 'sophia'
      END,
      '.',
      LOWER(CASE MOD(seq, 15)
        WHEN 0 THEN 'smith' WHEN 1 THEN 'johnson' WHEN 2 THEN 'williams' WHEN 3 THEN 'brown'
        WHEN 4 THEN 'jones' WHEN 5 THEN 'garcia' WHEN 6 THEN 'miller' WHEN 7 THEN 'davis'
        WHEN 8 THEN 'rodriguez' WHEN 9 THEN 'martinez' WHEN 10 THEN 'hernandez' WHEN 11 THEN 'lopez'
        WHEN 12 THEN 'gonzalez' WHEN 13 THEN 'wilson' ELSE 'anderson'
      END),
      '@example.com'
    ) as email,
    CONCAT('090-', LPAD(CAST(1000 + MOD(seq, 9000) AS STRING), 4, '0'), '-', LPAD(CAST(1000 + MOD(seq * 7, 9000) AS STRING), 4, '0')) as phone,
    TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL MOD(seq, 365) DAY) as created_at
  FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq
)
SELECT * FROM dummy_data;

-- =============================================================================
-- 2. raw_products (上流のみ・説明なし・論理名あり・データあり)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.raw_products` (
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

-- 1000件のダミーデータ挿入
INSERT INTO `tt_hackathon.raw_products`
WITH dummy_data AS (
  SELECT
    CONCAT('PROD', LPAD(CAST(seq AS STRING), 6, '0')) as product_id,
    CASE MOD(seq, 25)
      WHEN 0 THEN 'ノートパソコン' WHEN 1 THEN 'マウス' WHEN 2 THEN 'キーボード' WHEN 3 THEN 'モニター'
      WHEN 4 THEN 'スピーカー' WHEN 5 THEN 'ヘッドフォン' WHEN 6 THEN 'Webカメラ' WHEN 7 THEN 'プリンター'
      WHEN 8 THEN 'スマートフォン' WHEN 9 THEN 'タブレット' WHEN 10 THEN 'ハードディスク' WHEN 11 THEN 'SSD'
      WHEN 12 THEN 'メモリ' WHEN 13 THEN 'グラフィックカード' WHEN 14 THEN 'マザーボード' WHEN 15 THEN 'CPU'
      WHEN 16 THEN 'ケーブル' WHEN 17 THEN 'アダプター' WHEN 18 THEN 'バッテリー' WHEN 19 THEN 'ケース'
      WHEN 20 THEN 'スタンド' WHEN 21 THEN 'フィルム' WHEN 22 THEN 'クリーナー' WHEN 23 THEN 'ソフトウェア'
      ELSE 'アクセサリー'
    END as product_name,
    CASE MOD(seq, 8)
      WHEN 0 THEN 'Electronics' WHEN 1 THEN 'Computers' WHEN 2 THEN 'Mobile'
      WHEN 3 THEN 'Audio' WHEN 4 THEN 'Gaming' WHEN 5 THEN 'Office'
      WHEN 6 THEN 'Storage' ELSE 'Accessories'
    END as category,
    CAST((1000 + MOD(seq * 123, 99000)) AS NUMERIC) as price,
    10 + MOD(seq * 456, 500) as stock_quantity,
    TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL MOD(seq, 180) DAY) as created_at
  FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq
)
SELECT * FROM dummy_data;

-- =============================================================================
-- 3. raw_orders (上流のみ・説明あり・論理名なし・データNULL)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.raw_orders` (
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
INSERT INTO `tt_hackathon.raw_orders` VALUES
  ('ORD001', 'CUST001', CURRENT_TIMESTAMP(), 92780, 'completed', 'Normal order'),
  ('ORD002', NULL, CURRENT_TIMESTAMP(), NULL, 'pending', NULL),  -- NULLデータ
  ('ORD003', 'CUST003', NULL, 5980, NULL, 'Incomplete data');   -- NULLデータ

-- =============================================================================
-- 4. customer_profiles (上流・下流両方・説明あり・論理名あり・データあり)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.customer_profiles` (
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
CREATE OR REPLACE VIEW `tt_hackathon.customer_profiles_source` AS
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
FROM `tt_hackathon.raw_customers`;

-- サンプルデータ挿入
INSERT INTO `tt_hackathon.customer_profiles`
SELECT * FROM `tt_hackathon.customer_profiles_source`;

-- =============================================================================
-- 5. product_catalog (上流・下流両方・説明なし・論理名なし・データNULL)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.product_catalog` (
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
INSERT INTO `tt_hackathon.product_catalog` VALUES
  ('CAT001', 'PROD001', 'ノートパソコン', NULL, 'Electronics/Computers', 'premium', 'available', CURRENT_TIMESTAMP()),
  ('CAT002', NULL, NULL, NULL, NULL, NULL, NULL, NULL),  -- 全てNULL
  ('CAT003', 'PROD003', 'キーボード', 'Mechanical keyboard', NULL, 'standard', NULL, CURRENT_TIMESTAMP());

-- =============================================================================
-- 6. order_details (上流・下流両方・説明あり・論理名なし・データあり)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.order_details` (
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
INSERT INTO `tt_hackathon.order_details` VALUES
  ('DTL001', 'ORD001', 'CUST001', CURRENT_TIMESTAMP(), 92780, 'credit_card', '東京都渋谷区1-1-1', CURRENT_TIMESTAMP()),
  ('DTL002', 'ORD003', 'CUST003', CURRENT_TIMESTAMP(), 5980, 'bank_transfer', '大阪府大阪市2-2-2', CURRENT_TIMESTAMP());

-- =============================================================================
-- 7. order_items (上流・下流両方・説明なし・論理名あり・データあり)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.order_items` (
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
INSERT INTO `tt_hackathon.order_items` VALUES
  ('ITEM001', 'ORD001', 'PROD001', 1, 89800, 89800, 0, CURRENT_TIMESTAMP()),
  ('ITEM002', 'ORD001', 'PROD002', 1, 2980, 2980, 0, CURRENT_TIMESTAMP()),
  ('ITEM003', 'ORD003', 'PROD003', 1, 5980, 5980, 0, CURRENT_TIMESTAMP());

-- =============================================================================
-- 8. customer_analytics (下流のみ・説明あり・論理名あり・データNULL)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.customer_analytics` (
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
INSERT INTO `tt_hackathon.customer_analytics` VALUES
  ('ANAL001', 'CUST001', 92780, 92780, 1.0, 0.2, 85, CURRENT_TIMESTAMP()),
  ('ANAL002', 'CUST002', NULL, NULL, NULL, NULL, NULL, NULL),  -- 全てNULL（計算失敗）
  ('ANAL003', 'CUST003', 5980, 5980, NULL, 0.8, 45, CURRENT_TIMESTAMP());

-- =============================================================================
-- 9. sales_summary (下流のみ・説明なし・論理名なし・データあり)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.sales_summary` (
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
INSERT INTO `tt_hackathon.sales_summary` VALUES
  ('SUM001', CURRENT_DATE(), 2, 98760, 49380, 'Electronics', 2, CURRENT_TIMESTAMP()),
  ('SUM002', DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY), 1, 5980, 5980, 'Electronics', 1, CURRENT_TIMESTAMP());

-- =============================================================================
-- 10. monthly_reports (下流のみ・説明あり・論理名なし・データあり)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.monthly_reports` (
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
INSERT INTO `tt_hackathon.monthly_reports` VALUES
  ('RPT001', '2025-09', 3, 3, 2, 98760, ['PROD001', 'PROD003'], JSON '{"conversion_rate": 0.67, "customer_satisfaction": 4.2}', CURRENT_TIMESTAMP());

-- =============================================================================
-- 依存関係を明確にするためのビュー作成
-- =============================================================================

-- customer_analytics ← customer_profiles の依存関係
CREATE OR REPLACE VIEW `tt_hackathon.customer_analytics_base` AS
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
FROM `tt_hackathon.customer_profiles`;

-- sales_summary ← order_details, order_items の依存関係
CREATE OR REPLACE VIEW `tt_hackathon.sales_summary_base` AS
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
  FROM `tt_hackathon.order_details` od
  GROUP BY DATE(od.order_date)
);

-- monthly_reports ← sales_summary, customer_analytics の依存関係
CREATE OR REPLACE VIEW `tt_hackathon.monthly_reports_base` AS
SELECT
  CONCAT('RPT_', FORMAT_DATE('%Y%m', CURRENT_DATE())) as report_id,
  FORMAT_DATE('%Y-%m', CURRENT_DATE()) as report_month,
  (SELECT COUNT(*) FROM `tt_hackathon.customer_profiles`) as total_customers,
  (SELECT COUNT(*) FROM `tt_hackathon.customer_profiles`) as new_customers,
  (SELECT SUM(total_orders) FROM `tt_hackathon.sales_summary`) as total_orders,
  (SELECT SUM(total_revenue) FROM `tt_hackathon.sales_summary`) as total_revenue,
  ['PROD001', 'PROD002', 'PROD003'] as top_products,
  JSON '{"conversion_rate": 0.75, "customer_satisfaction": 4.5}' as kpi_metrics,
  CURRENT_TIMESTAMP() as generated_at;

-- =============================================================================
-- 追加テーブル（11-60）: 50個の新しいテーブル
-- 各テーブルに1000件のダミーデータを挿入
-- =============================================================================

-- =============================================================================
-- 11. user_sessions (ユーザーセッション管理)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.user_sessions` (
  session_id STRING,
  user_id STRING,
  login_time TIMESTAMP,
  logout_time TIMESTAMP,
  ip_address STRING,
  user_agent STRING,
  device_type STRING,
  session_duration_minutes INT64,
  page_views INT64,
  created_at TIMESTAMP
)
OPTIONS(
  description="ユーザーセッション情報。ログイン・ログアウト時間、デバイス情報、セッション継続時間を記録。",
  labels=[
    ("logical_name", "user_session_tracking_table"),
    ("data_type", "behavioral"),
    ("privacy_level", "medium")
  ]
);

-- 1000件のダミーデータ挿入
INSERT INTO `tt_hackathon.user_sessions`
WITH dummy_data AS (
  SELECT
    CONCAT('SESS', LPAD(CAST(seq AS STRING), 6, '0')) as session_id,
    CONCAT('USER', LPAD(CAST(1 + MOD(seq, 500) AS STRING), 6, '0')) as user_id,
    TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL MOD(seq, 30) DAY) as login_time,
    CASE WHEN MOD(seq, 10) = 0 THEN NULL
         ELSE TIMESTAMP_ADD(TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL MOD(seq, 30) DAY), INTERVAL (30 + MOD(seq, 240)) MINUTE)
    END as logout_time,
    CONCAT('192.168.', CAST(1 + MOD(seq, 254) AS STRING), '.', CAST(1 + MOD(seq * 7, 254) AS STRING)) as ip_address,
    CASE MOD(seq, 5)
      WHEN 0 THEN 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      WHEN 1 THEN 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
      WHEN 2 THEN 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15'
      WHEN 3 THEN 'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0'
      ELSE 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    END as user_agent,
    CASE MOD(seq, 4)
      WHEN 0 THEN 'Desktop' WHEN 1 THEN 'Mobile' WHEN 2 THEN 'Tablet' ELSE 'Unknown'
    END as device_type,
    30 + MOD(seq, 240) as session_duration_minutes,
    1 + MOD(seq, 50) as page_views,
    TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL MOD(seq, 30) DAY) as created_at
  FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq
)
SELECT * FROM dummy_data;

-- =============================================================================
-- 12. inventory_movements (在庫移動履歴)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.inventory_movements` (
  movement_id STRING,
  product_id STRING,
  warehouse_id STRING,
  movement_type STRING,
  quantity_change INT64,
  previous_quantity INT64,
  new_quantity INT64,
  reason STRING,
  employee_id STRING,
  movement_date TIMESTAMP
)
OPTIONS(
  description="在庫移動履歴。入庫・出庫・調整などの在庫変動を記録。",
  labels=[
    ("logical_name", "inventory_movement_log"),
    ("data_type", "transactional"),
    ("business_critical", "true")
  ]
);

-- 1000件のダミーデータ挿入
INSERT INTO `tt_hackathon.inventory_movements`
WITH dummy_data AS (
  SELECT
    CONCAT('MOV', LPAD(CAST(seq AS STRING), 6, '0')) as movement_id,
    CONCAT('PROD', LPAD(CAST(1 + MOD(seq, 1000) AS STRING), 6, '0')) as product_id,
    CONCAT('WH', LPAD(CAST(1 + MOD(seq, 10) AS STRING), 3, '0')) as warehouse_id,
    CASE MOD(seq, 6)
      WHEN 0 THEN 'IN' WHEN 1 THEN 'OUT' WHEN 2 THEN 'ADJUSTMENT'
      WHEN 3 THEN 'TRANSFER' WHEN 4 THEN 'RETURN' ELSE 'DAMAGE'
    END as movement_type,
    CASE MOD(seq, 6)
      WHEN 0 THEN (1 + MOD(seq, 100))  -- IN: positive
      WHEN 1 THEN -(1 + MOD(seq, 50))  -- OUT: negative
      ELSE (MOD(seq, 21) - 10)  -- Others: can be positive or negative
    END as quantity_change,
    50 + MOD(seq * 123, 200) as previous_quantity,
    (50 + MOD(seq * 123, 200)) + CASE MOD(seq, 6)
      WHEN 0 THEN (1 + MOD(seq, 100))
      WHEN 1 THEN -(1 + MOD(seq, 50))
      ELSE (MOD(seq, 21) - 10)
    END as new_quantity,
    CASE MOD(seq, 8)
      WHEN 0 THEN 'Purchase order' WHEN 1 THEN 'Sale' WHEN 2 THEN 'Stock count adjustment'
      WHEN 3 THEN 'Warehouse transfer' WHEN 4 THEN 'Customer return' WHEN 5 THEN 'Damaged goods'
      WHEN 6 THEN 'Expired items' ELSE 'System correction'
    END as reason,
    CONCAT('EMP', LPAD(CAST(1 + MOD(seq, 50) AS STRING), 4, '0')) as employee_id,
    TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL MOD(seq, 90) DAY) as movement_date
  FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq
)
SELECT * FROM dummy_data;

-- =============================================================================
-- 13. payment_transactions (決済取引履歴)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.payment_transactions` (
  transaction_id STRING,
  order_id STRING,
  customer_id STRING,
  payment_method STRING,
  amount NUMERIC,
  currency STRING,
  status STRING,
  gateway_response STRING,
  transaction_fee NUMERIC,
  processed_at TIMESTAMP
)
OPTIONS(
  description="決済取引履歴。クレジットカード、銀行振込等の決済情報を記録。",
  labels=[
    ("logical_name", "payment_transaction_log"),
    ("data_type", "financial"),
    ("pii_data", "true"),
    ("security_level", "high")
  ]
);

-- 1000件のダミーデータ挿入
INSERT INTO `tt_hackathon.payment_transactions`
WITH dummy_data AS (
  SELECT
    CONCAT('TXN', LPAD(CAST(seq AS STRING), 6, '0')) as transaction_id,
    CONCAT('ORD', LPAD(CAST(1 + MOD(seq, 800) AS STRING), 6, '0')) as order_id,
    CONCAT('CUST', LPAD(CAST(1 + MOD(seq, 1000) AS STRING), 6, '0')) as customer_id,
    CASE MOD(seq, 5)
      WHEN 0 THEN 'credit_card' WHEN 1 THEN 'debit_card' WHEN 2 THEN 'bank_transfer'
      WHEN 3 THEN 'digital_wallet' ELSE 'cash'
    END as payment_method,
    CAST((1000 + MOD(seq * 789, 50000)) AS NUMERIC) as amount,
    'JPY' as currency,
    CASE MOD(seq, 10)
      WHEN 0 THEN 'pending' WHEN 1 THEN 'failed' WHEN 8 THEN 'cancelled'
      ELSE 'completed'
    END as status,
    CASE MOD(seq, 10)
      WHEN 0 THEN 'PENDING' WHEN 1 THEN 'DECLINED' WHEN 8 THEN 'CANCELLED'
      ELSE 'APPROVED'
    END as gateway_response,
    CAST((30 + MOD(seq, 100)) AS NUMERIC) as transaction_fee,
    TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL MOD(seq, 60) DAY) as processed_at
  FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq
)
SELECT * FROM dummy_data;

-- =============================================================================
-- 14. shipping_records (配送記録)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.shipping_records` (
  shipping_id STRING,
  order_id STRING,
  tracking_number STRING,
  carrier STRING,
  shipping_method STRING,
  origin_address STRING,
  destination_address STRING,
  shipped_date TIMESTAMP,
  delivered_date TIMESTAMP,
  status STRING
)
OPTIONS(
  description="配送記録。注文の配送状況、追跡番号、配送業者情報を管理。"
);

-- 1000件のダミーデータ挿入
INSERT INTO `tt_hackathon.shipping_records`
WITH dummy_data AS (
  SELECT
    CONCAT('SHIP', LPAD(CAST(seq AS STRING), 6, '0')) as shipping_id,
    CONCAT('ORD', LPAD(CAST(1 + MOD(seq, 800) AS STRING), 6, '0')) as order_id,
    CONCAT('TRK', LPAD(CAST(seq * 12345 AS STRING), 12, '0')) as tracking_number,
    CASE MOD(seq, 4)
      WHEN 0 THEN 'ヤマト運輸' WHEN 1 THEN '佐川急便' WHEN 2 THEN '日本郵便' ELSE 'DHL'
    END as carrier,
    CASE MOD(seq, 3)
      WHEN 0 THEN 'standard' WHEN 1 THEN 'express' ELSE 'overnight'
    END as shipping_method,
    '東京都千代田区1-1-1 配送センター' as origin_address,
    CONCAT(
      CASE MOD(seq, 8)
        WHEN 0 THEN '東京都渋谷区' WHEN 1 THEN '大阪府大阪市' WHEN 2 THEN '愛知県名古屋市'
        WHEN 3 THEN '神奈川県横浜市' WHEN 4 THEN '福岡県福岡市' WHEN 5 THEN '北海道札幌市'
        WHEN 6 THEN '宮城県仙台市' ELSE '広島県広島市'
      END,
      CAST(1 + MOD(seq, 10) AS STRING), '-',
      CAST(1 + MOD(seq * 7, 10) AS STRING), '-',
      CAST(1 + MOD(seq * 13, 20) AS STRING)
    ) as destination_address,
    TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL MOD(seq, 30) DAY) as shipped_date,
    CASE WHEN MOD(seq, 15) = 0 THEN NULL
         ELSE TIMESTAMP_ADD(TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL MOD(seq, 30) DAY), INTERVAL (1 + MOD(seq, 7)) DAY)
    END as delivered_date,
    CASE MOD(seq, 8)
      WHEN 0 THEN 'preparing' WHEN 1 THEN 'shipped' WHEN 2 THEN 'in_transit'
      WHEN 3 THEN 'out_for_delivery' WHEN 4 THEN 'delivered' WHEN 5 THEN 'failed_delivery'
      WHEN 6 THEN 'returned' ELSE 'cancelled'
    END as status
  FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq
)
SELECT * FROM dummy_data;

-- =============================================================================
-- 15. product_reviews (商品レビュー)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.product_reviews` (
  review_id STRING,
  product_id STRING,
  customer_id STRING,
  rating INT64,
  title STRING,
  comment STRING,
  helpful_votes INT64,
  verified_purchase BOOL,
  review_date TIMESTAMP
)
OPTIONS(
  labels=[
    ("logical_name", "product_review_feedback"),
    ("data_type", "user_generated"),
    ("sentiment_analysis", "enabled")
  ]
);

-- 1000件のダミーデータ挿入
INSERT INTO `tt_hackathon.product_reviews`
WITH dummy_data AS (
  SELECT
    CONCAT('REV', LPAD(CAST(seq AS STRING), 6, '0')) as review_id,
    CONCAT('PROD', LPAD(CAST(1 + MOD(seq, 1000) AS STRING), 6, '0')) as product_id,
    CONCAT('CUST', LPAD(CAST(1 + MOD(seq, 1000) AS STRING), 6, '0')) as customer_id,
    1 + MOD(seq, 5) as rating,
    CASE MOD(seq, 10)
      WHEN 0 THEN '素晴らしい商品です' WHEN 1 THEN '期待通りでした' WHEN 2 THEN 'コスパが良い'
      WHEN 3 THEN '使いやすいです' WHEN 4 THEN '品質に満足' WHEN 5 THEN 'おすすめします'
      WHEN 6 THEN '普通です' WHEN 7 THEN 'もう少し改善を' WHEN 8 THEN '価格が高い'
      ELSE '不満があります'
    END as title,
    CASE MOD(seq, 8)
      WHEN 0 THEN '非常に満足しています。品質も良く、配送も早かったです。'
      WHEN 1 THEN '期待していた通りの商品でした。また購入したいと思います。'
      WHEN 2 THEN 'コストパフォーマンスが良く、機能も十分です。'
      WHEN 3 THEN '使いやすく、デザインも気に入っています。'
      WHEN 4 THEN '品質は良いですが、もう少し安ければ良いと思います。'
      WHEN 5 THEN '普通の商品です。特に問題はありませんが、特別良いわけでもありません。'
      WHEN 6 THEN '期待していたほどではありませんでした。'
      ELSE '不具合があり、返品を検討しています。'
    END as comment,
    MOD(seq, 20) as helpful_votes,
    MOD(seq, 4) != 0 as verified_purchase,
    TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL MOD(seq, 180) DAY) as review_date
  FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq
)
SELECT * FROM dummy_data;

-- =============================================================================
-- 16. supplier_information (サプライヤー情報)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.supplier_information` (
  supplier_id STRING,
  company_name STRING,
  contact_person STRING,
  email STRING,
  phone STRING,
  address STRING,
  country STRING,
  contract_start_date DATE,
  contract_end_date DATE,
  payment_terms STRING,
  quality_rating NUMERIC
)
OPTIONS(
  description="サプライヤー情報。取引先企業の基本情報、契約条件、品質評価を管理。",
  labels=[
    ("logical_name", "supplier_master_data"),
    ("data_type", "master"),
    ("business_critical", "true")
  ]
);

-- 1000件のダミーデータ挿入
INSERT INTO `tt_hackathon.supplier_information`
WITH dummy_data AS (
  SELECT
    CONCAT('SUP', LPAD(CAST(seq AS STRING), 6, '0')) as supplier_id,
    CONCAT(
      CASE MOD(seq, 15)
        WHEN 0 THEN 'テクノロジー' WHEN 1 THEN 'エレクトロニクス' WHEN 2 THEN 'システムズ'
        WHEN 3 THEN 'インダストリー' WHEN 4 THEN 'マニュファクチャリング' WHEN 5 THEN 'コーポレーション'
        WHEN 6 THEN 'エンタープライズ' WHEN 7 THEN 'ソリューションズ' WHEN 8 THEN 'イノベーション'
        WHEN 9 THEN 'グローバル' WHEN 10 THEN 'アドバンスド' WHEN 11 THEN 'プレミアム'
        WHEN 12 THEN 'スマート' WHEN 13 THEN 'デジタル' ELSE 'フューチャー'
      END,
      ' ',
      CASE MOD(seq, 10)
        WHEN 0 THEN '株式会社' WHEN 1 THEN '有限会社' WHEN 2 THEN '合同会社'
        WHEN 3 THEN 'Co., Ltd.' WHEN 4 THEN 'Inc.' WHEN 5 THEN 'Corp.'
        WHEN 6 THEN 'LLC' WHEN 7 THEN 'Ltd.' WHEN 8 THEN 'GmbH'
        ELSE 'S.A.'
      END
    ) as company_name,
    CONCAT(
      CASE MOD(seq, 12)
        WHEN 0 THEN '田中' WHEN 1 THEN '佐藤' WHEN 2 THEN '鈴木' WHEN 3 THEN '高橋'
        WHEN 4 THEN '渡辺' WHEN 5 THEN '伊藤' WHEN 6 THEN '山田' WHEN 7 THEN '中村'
        WHEN 8 THEN '小林' WHEN 9 THEN '加藤' WHEN 10 THEN '吉田' ELSE '山本'
      END,
      ' ',
      CASE MOD(seq, 8)
        WHEN 0 THEN '太郎' WHEN 1 THEN '次郎' WHEN 2 THEN '三郎' WHEN 3 THEN '四郎'
        WHEN 4 THEN '花子' WHEN 5 THEN '美子' WHEN 6 THEN '和子' ELSE '恵子'
      END
    ) as contact_person,
    CONCAT('contact', CAST(seq AS STRING), '@supplier', CAST(MOD(seq, 100) AS STRING), '.com') as email,
    CONCAT('03-', LPAD(CAST(1000 + MOD(seq, 9000) AS STRING), 4, '0'), '-', LPAD(CAST(1000 + MOD(seq * 7, 9000) AS STRING), 4, '0')) as phone,
    CONCAT(
      CASE MOD(seq, 6)
        WHEN 0 THEN '東京都港区' WHEN 1 THEN '大阪府大阪市' WHEN 2 THEN '愛知県名古屋市'
        WHEN 3 THEN '神奈川県横浜市' WHEN 4 THEN '福岡県福岡市' ELSE '北海道札幌市'
      END,
      CAST(1 + MOD(seq, 10) AS STRING), '-',
      CAST(1 + MOD(seq * 3, 10) AS STRING), '-',
      CAST(1 + MOD(seq * 5, 20) AS STRING)
    ) as address,
    CASE MOD(seq, 8)
      WHEN 0 THEN 'Japan' WHEN 1 THEN 'China' WHEN 2 THEN 'South Korea'
      WHEN 3 THEN 'Taiwan' WHEN 4 THEN 'Singapore' WHEN 5 THEN 'Thailand'
      WHEN 6 THEN 'Vietnam' ELSE 'Malaysia'
    END as country,
    DATE_SUB(CURRENT_DATE(), INTERVAL MOD(seq, 1000) DAY) as contract_start_date,
    DATE_ADD(DATE_SUB(CURRENT_DATE(), INTERVAL MOD(seq, 1000) DAY), INTERVAL (365 + MOD(seq, 730)) DAY) as contract_end_date,
    CASE MOD(seq, 4)
      WHEN 0 THEN 'Net 30' WHEN 1 THEN 'Net 60' WHEN 2 THEN 'Net 90' ELSE 'COD'
    END as payment_terms,
    CAST((3.0 + (MOD(seq, 20) / 10.0)) AS NUMERIC) as quality_rating
  FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq
)
SELECT * FROM dummy_data;

-- =============================================================================
-- 17. employee_records (従業員記録)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.employee_records` (
  employee_id STRING,
  first_name STRING,
  last_name STRING,
  email STRING,
  department STRING,
  position STRING,
  hire_date DATE,
  salary NUMERIC,
  manager_id STRING,
  status STRING
)
OPTIONS(
  description="従業員記録。人事情報、部署、役職、給与情報を管理。",
  labels=[
    ("logical_name", "employee_master_data"),
    ("data_type", "hr"),
    ("pii_data", "true"),
    ("confidential", "true")
  ]
);

-- 1000件のダミーデータ挿入
INSERT INTO `tt_hackathon.employee_records`
WITH dummy_data AS (
  SELECT
    CONCAT('EMP', LPAD(CAST(seq AS STRING), 4, '0')) as employee_id,
    CASE MOD(seq, 20)
      WHEN 0 THEN 'Hiroshi' WHEN 1 THEN 'Yuki' WHEN 2 THEN 'Takeshi' WHEN 3 THEN 'Akiko'
      WHEN 4 THEN 'Kenji' WHEN 5 THEN 'Naomi' WHEN 6 THEN 'Satoshi' WHEN 7 THEN 'Miyuki'
      WHEN 8 THEN 'Masaki' WHEN 9 THEN 'Emi' WHEN 10 THEN 'Daisuke' WHEN 11 THEN 'Yoko'
      WHEN 12 THEN 'Kazuki' WHEN 13 THEN 'Rei' WHEN 14 THEN 'Shinji' WHEN 15 THEN 'Maki'
      WHEN 16 THEN 'Ryota' WHEN 17 THEN 'Ai' WHEN 18 THEN 'Kenta' ELSE 'Saki'
    END as first_name,
    CASE MOD(seq, 15)
      WHEN 0 THEN 'Tanaka' WHEN 1 THEN 'Sato' WHEN 2 THEN 'Suzuki' WHEN 3 THEN 'Takahashi'
      WHEN 4 THEN 'Watanabe' WHEN 5 THEN 'Ito' WHEN 6 THEN 'Yamada' WHEN 7 THEN 'Nakamura'
      WHEN 8 THEN 'Kobayashi' WHEN 9 THEN 'Kato' WHEN 10 THEN 'Yoshida' WHEN 11 THEN 'Yamamoto'
      WHEN 12 THEN 'Sasaki' WHEN 13 THEN 'Matsumoto' ELSE 'Inoue'
    END as last_name,
    CONCAT(
      LOWER(CASE MOD(seq, 20)
        WHEN 0 THEN 'hiroshi' WHEN 1 THEN 'yuki' WHEN 2 THEN 'takeshi' WHEN 3 THEN 'akiko'
        WHEN 4 THEN 'kenji' WHEN 5 THEN 'naomi' WHEN 6 THEN 'satoshi' WHEN 7 THEN 'miyuki'
        WHEN 8 THEN 'masaki' WHEN 9 THEN 'emi' WHEN 10 THEN 'daisuke' WHEN 11 THEN 'yoko'
        WHEN 12 THEN 'kazuki' WHEN 13 THEN 'rei' WHEN 14 THEN 'shinji' WHEN 15 THEN 'maki'
        WHEN 16 THEN 'ryota' WHEN 17 THEN 'ai' WHEN 18 THEN 'kenta' ELSE 'saki'
      END),
      '.',
      LOWER(CASE MOD(seq, 15)
        WHEN 0 THEN 'tanaka' WHEN 1 THEN 'sato' WHEN 2 THEN 'suzuki' WHEN 3 THEN 'takahashi'
        WHEN 4 THEN 'watanabe' WHEN 5 THEN 'ito' WHEN 6 THEN 'yamada' WHEN 7 THEN 'nakamura'
        WHEN 8 THEN 'kobayashi' WHEN 9 THEN 'kato' WHEN 10 THEN 'yoshida' WHEN 11 THEN 'yamamoto'
        WHEN 12 THEN 'sasaki' WHEN 13 THEN 'matsumoto' ELSE 'inoue'
      END),
      '@company.com'
    ) as email,
    CASE MOD(seq, 8)
      WHEN 0 THEN 'Engineering' WHEN 1 THEN 'Sales' WHEN 2 THEN 'Marketing'
      WHEN 3 THEN 'HR' WHEN 4 THEN 'Finance' WHEN 5 THEN 'Operations'
      WHEN 6 THEN 'Customer Support' ELSE 'Legal'
    END as department,
    CASE MOD(seq, 12)
      WHEN 0 THEN 'Software Engineer' WHEN 1 THEN 'Sales Representative' WHEN 2 THEN 'Marketing Specialist'
      WHEN 3 THEN 'HR Coordinator' WHEN 4 THEN 'Financial Analyst' WHEN 5 THEN 'Operations Manager'
      WHEN 6 THEN 'Support Agent' WHEN 7 THEN 'Legal Counsel' WHEN 8 THEN 'Senior Engineer'
      WHEN 9 THEN 'Sales Manager' WHEN 10 THEN 'Marketing Manager' ELSE 'Director'
    END as position,
    DATE_SUB(CURRENT_DATE(), INTERVAL MOD(seq, 2000) DAY) as hire_date,
    CAST((3000000 + MOD(seq * 12345, 7000000)) AS NUMERIC) as salary,
    CASE WHEN seq <= 50 THEN NULL
         ELSE CONCAT('EMP', LPAD(CAST(1 + MOD(seq, 50) AS STRING), 4, '0'))
    END as manager_id,
    CASE MOD(seq, 20)
      WHEN 0 THEN 'inactive' WHEN 19 THEN 'terminated' ELSE 'active'
    END as status
  FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq
)
SELECT * FROM dummy_data;

-- =============================================================================
-- 18. marketing_campaigns (マーケティングキャンペーン)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.marketing_campaigns` (
  campaign_id STRING,
  campaign_name STRING,
  campaign_type STRING,
  start_date DATE,
  end_date DATE,
  budget NUMERIC,
  target_audience STRING,
  channel STRING,
  status STRING,
  created_by STRING
)
OPTIONS(
  labels=[
    ("logical_name", "marketing_campaign_master"),
    ("data_type", "marketing"),
    ("business_value", "high")
  ]
);

-- 1000件のダミーデータ挿入
INSERT INTO `tt_hackathon.marketing_campaigns`
WITH dummy_data AS (
  SELECT
    CONCAT('CAMP', LPAD(CAST(seq AS STRING), 6, '0')) as campaign_id,
    CONCAT(
      CASE MOD(seq, 10)
        WHEN 0 THEN 'Spring Sale' WHEN 1 THEN 'Summer Festival' WHEN 2 THEN 'Autumn Special'
        WHEN 3 THEN 'Winter Campaign' WHEN 4 THEN 'New Year Promotion' WHEN 5 THEN 'Back to School'
        WHEN 6 THEN 'Holiday Special' WHEN 7 THEN 'Flash Sale' WHEN 8 THEN 'Member Exclusive'
        ELSE 'Limited Time Offer'
      END,
      ' 2025-', LPAD(CAST(seq AS STRING), 3, '0')
    ) as campaign_name,
    CASE MOD(seq, 6)
      WHEN 0 THEN 'promotional' WHEN 1 THEN 'brand_awareness' WHEN 2 THEN 'product_launch'
      WHEN 3 THEN 'retention' WHEN 4 THEN 'acquisition' ELSE 'seasonal'
    END as campaign_type,
    DATE_SUB(CURRENT_DATE(), INTERVAL MOD(seq, 180) DAY) as start_date,
    DATE_ADD(DATE_SUB(CURRENT_DATE(), INTERVAL MOD(seq, 180) DAY), INTERVAL (7 + MOD(seq, 30)) DAY) as end_date,
    CAST((100000 + MOD(seq * 456, 900000)) AS NUMERIC) as budget,
    CASE MOD(seq, 8)
      WHEN 0 THEN '20-30代女性' WHEN 1 THEN '30-40代男性' WHEN 2 THEN '学生'
      WHEN 3 THEN 'ビジネスパーソン' WHEN 4 THEN 'シニア層' WHEN 5 THEN 'ファミリー'
      WHEN 6 THEN 'IT関係者' ELSE '全年齢'
    END as target_audience,
    CASE MOD(seq, 7)
      WHEN 0 THEN 'email' WHEN 1 THEN 'social_media' WHEN 2 THEN 'web_ads'
      WHEN 3 THEN 'tv' WHEN 4 THEN 'radio' WHEN 5 THEN 'print' ELSE 'outdoor'
    END as channel,
    CASE MOD(seq, 5)
      WHEN 0 THEN 'planning' WHEN 1 THEN 'active' WHEN 2 THEN 'paused'
      WHEN 3 THEN 'completed' ELSE 'cancelled'
    END as status,
    CONCAT('EMP', LPAD(CAST(1 + MOD(seq, 50) AS STRING), 4, '0')) as created_by
  FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq
)
SELECT * FROM dummy_data;

-- =============================================================================
-- 19. website_analytics (ウェブサイト分析)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.website_analytics` (
  analytics_id STRING,
  session_id STRING,
  page_url STRING,
  page_title STRING,
  visit_time TIMESTAMP,
  time_on_page INT64,
  bounce_rate NUMERIC,
  conversion_flag BOOL,
  referrer_url STRING,
  user_agent STRING
)
OPTIONS(
  description="ウェブサイト分析データ。ページビュー、セッション時間、コンバージョン率を記録。"
);

-- 1000件のダミーデータ挿入
INSERT INTO `tt_hackathon.website_analytics`
WITH dummy_data AS (
  SELECT
    CONCAT('WEB', LPAD(CAST(seq AS STRING), 6, '0')) as analytics_id,
    CONCAT('SESS', LPAD(CAST(1 + MOD(seq, 1000) AS STRING), 6, '0')) as session_id,
    CONCAT('https://example.com/',
      CASE MOD(seq, 15)
        WHEN 0 THEN 'home' WHEN 1 THEN 'products' WHEN 2 THEN 'about'
        WHEN 3 THEN 'contact' WHEN 4 THEN 'cart' WHEN 5 THEN 'checkout'
        WHEN 6 THEN 'login' WHEN 7 THEN 'register' WHEN 8 THEN 'search'
        WHEN 9 THEN 'category/electronics' WHEN 10 THEN 'category/computers'
        WHEN 11 THEN 'product/detail' WHEN 12 THEN 'support' WHEN 13 THEN 'blog'
        ELSE 'news'
      END
    ) as page_url,
    CASE MOD(seq, 15)
      WHEN 0 THEN 'ホーム' WHEN 1 THEN '商品一覧' WHEN 2 THEN '会社概要'
      WHEN 3 THEN 'お問い合わせ' WHEN 4 THEN 'ショッピングカート' WHEN 5 THEN 'チェックアウト'
      WHEN 6 THEN 'ログイン' WHEN 7 THEN '新規登録' WHEN 8 THEN '検索結果'
      WHEN 9 THEN 'エレクトロニクス' WHEN 10 THEN 'コンピューター'
      WHEN 11 THEN '商品詳細' WHEN 12 THEN 'サポート' WHEN 13 THEN 'ブログ'
      ELSE 'ニュース'
    END as page_title,
    TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL MOD(seq, 30) DAY) as visit_time,
    15 + MOD(seq, 300) as time_on_page,
    CAST((MOD(seq, 100) / 100.0) AS NUMERIC) as bounce_rate,
    MOD(seq, 20) = 0 as conversion_flag,
    CASE MOD(seq, 8)
      WHEN 0 THEN 'https://google.com/search' WHEN 1 THEN 'https://yahoo.co.jp/search'
      WHEN 2 THEN 'https://facebook.com' WHEN 3 THEN 'https://twitter.com'
      WHEN 4 THEN 'https://instagram.com' WHEN 5 THEN 'direct'
      WHEN 6 THEN 'email' ELSE 'other'
    END as referrer_url,
    CASE MOD(seq, 4)
      WHEN 0 THEN 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      WHEN 1 THEN 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
      WHEN 2 THEN 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15'
      ELSE 'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0'
    END as user_agent
  FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq
)
SELECT * FROM dummy_data;

-- =============================================================================
-- 20. financial_transactions (財務取引)
-- =============================================================================
CREATE OR REPLACE TABLE `tt_hackathon.financial_transactions` (
  transaction_id STRING,
  account_id STRING,
  transaction_type STRING,
  amount NUMERIC,
  currency STRING,
  description STRING,
  category STRING,
  transaction_date TIMESTAMP,
  balance_after NUMERIC,
  created_by STRING
)
OPTIONS(
  description="財務取引記録。収入・支出・振替等の会計取引を記録。",
  labels=[
    ("logical_name", "financial_transaction_log"),
    ("data_type", "financial"),
    ("audit_required", "true"),
    ("confidential", "true")
  ]
);

-- 1000件のダミーデータ挿入
INSERT INTO `tt_hackathon.financial_transactions`
WITH dummy_data AS (
  SELECT
    CONCAT('FIN', LPAD(CAST(seq AS STRING), 6, '0')) as transaction_id,
    CONCAT('ACC', LPAD(CAST(1 + MOD(seq, 20) AS STRING), 3, '0')) as account_id,
    CASE MOD(seq, 6)
      WHEN 0 THEN 'income' WHEN 1 THEN 'expense' WHEN 2 THEN 'transfer'
      WHEN 3 THEN 'investment' WHEN 4 THEN 'loan' ELSE 'adjustment'
    END as transaction_type,
    CASE MOD(seq, 6)
      WHEN 0 THEN CAST((10000 + MOD(seq * 789, 500000)) AS NUMERIC)  -- income: positive
      WHEN 1 THEN CAST(-(1000 + MOD(seq * 456, 100000)) AS NUMERIC)  -- expense: negative
      ELSE CAST((MOD(seq * 123, 200000) - 100000) AS NUMERIC)  -- others: can be positive or negative
    END as amount,
    'JPY' as currency,
    CASE MOD(seq, 12)
      WHEN 0 THEN '売上収入' WHEN 1 THEN '事務用品購入' WHEN 2 THEN '口座間振替'
      WHEN 3 THEN '設備投資' WHEN 4 THEN '銀行借入' WHEN 5 THEN '給与支払い'
      WHEN 6 THEN '広告費' WHEN 7 THEN '光熱費' WHEN 8 THEN '通信費'
      WHEN 9 THEN '交通費' WHEN 10 THEN '会議費' ELSE '雑費'
    END as description,
    CASE MOD(seq, 8)
      WHEN 0 THEN 'revenue' WHEN 1 THEN 'office_supplies' WHEN 2 THEN 'transfer'
      WHEN 3 THEN 'equipment' WHEN 4 THEN 'loan' WHEN 5 THEN 'payroll'
      WHEN 6 THEN 'marketing' ELSE 'utilities'
    END as category,
    TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL MOD(seq, 90) DAY) as transaction_date,
    CAST((1000000 + MOD(seq * 987, 5000000)) AS NUMERIC) as balance_after,
    CONCAT('EMP', LPAD(CAST(1 + MOD(seq, 20) AS STRING), 4, '0')) as created_by
  FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq
)
SELECT * FROM dummy_data;

-- =============================================================================
-- 追加テーブル（21-60）: 残り40個のテーブル
-- 各テーブルに1000件のダミーデータを挿入
-- =============================================================================

-- 21. audit_logs (監査ログ)
CREATE OR REPLACE TABLE `tt_hackathon.audit_logs` (
  log_id STRING, user_id STRING, action STRING, table_name STRING,
  record_id STRING, old_values JSON, new_values JSON, timestamp TIMESTAMP
)
OPTIONS(description="システム監査ログ。データ変更履歴を記録。", labels=[("data_type", "audit"), ("retention", "7_years")]);

INSERT INTO `tt_hackathon.audit_logs`
SELECT
  CONCAT('LOG', LPAD(CAST(seq AS STRING), 6, '0')),
  CONCAT('USER', LPAD(CAST(1 + MOD(seq, 100) AS STRING), 6, '0')),
  CASE MOD(seq, 4) WHEN 0 THEN 'INSERT' WHEN 1 THEN 'UPDATE' WHEN 2 THEN 'DELETE' ELSE 'SELECT' END,
  CASE MOD(seq, 10) WHEN 0 THEN 'customers' WHEN 1 THEN 'products' WHEN 2 THEN 'orders' ELSE 'users' END,
  CONCAT('REC', CAST(seq AS STRING)),
  JSON '{"old": "value"}', JSON '{"new": "value"}',
  TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL MOD(seq, 30) DAY)
FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;

-- 22-60. 残り39テーブル（効率的実装）
CREATE OR REPLACE TABLE `tt_hackathon.system_metrics` (metric_id STRING, service_name STRING, metric_name STRING, metric_value NUMERIC, unit STRING, timestamp TIMESTAMP, host STRING, environment STRING) OPTIONS(labels=[("data_type", "monitoring"), ("real_time", "true")]);
CREATE OR REPLACE TABLE `tt_hackathon.notification_history` (notification_id STRING, user_id STRING, type STRING, title STRING, message STRING, channel STRING, status STRING, sent_at TIMESTAMP) OPTIONS(description="通知送信履歴。メール、SMS、プッシュ通知の配信記録。");
CREATE OR REPLACE TABLE `tt_hackathon.api_usage_logs` (log_id STRING, api_key STRING, endpoint STRING, method STRING, status_code INT64, response_time_ms INT64, request_size_bytes INT64, timestamp TIMESTAMP) OPTIONS(labels=[("data_type", "api_logs"), ("monitoring", "enabled")]);
CREATE OR REPLACE TABLE `tt_hackathon.backup_records` (backup_id STRING, table_name STRING, backup_type STRING, file_path STRING, file_size_gb NUMERIC, status STRING, started_at TIMESTAMP, completed_at TIMESTAMP) OPTIONS(description="データベースバックアップ記録。バックアップ作成履歴と復旧情報。", labels=[("data_type", "backup")]);
CREATE OR REPLACE TABLE `tt_hackathon.security_events` (event_id STRING, user_id STRING, event_type STRING, severity STRING, description STRING, ip_address STRING, user_agent STRING, timestamp TIMESTAMP) OPTIONS(labels=[("data_type", "security"), ("alert_enabled", "true")]);
CREATE OR REPLACE TABLE `tt_hackathon.performance_metrics` (metric_id STRING, query_id STRING, execution_time_ms INT64, rows_processed INT64, bytes_processed INT64, cpu_usage NUMERIC, memory_usage NUMERIC, timestamp TIMESTAMP) OPTIONS(description="クエリパフォーマンス指標。実行時間、処理行数、リソース使用量を記録。");
CREATE OR REPLACE TABLE `tt_hackathon.data_quality_checks` (check_id STRING, table_name STRING, column_name STRING, rule_name STRING, expected_value STRING, actual_value STRING, status STRING, checked_at TIMESTAMP) OPTIONS(labels=[("data_type", "quality"), ("automated", "true")]);
CREATE OR REPLACE TABLE `tt_hackathon.user_preferences` (preference_id STRING, user_id STRING, category STRING, setting_name STRING, setting_value STRING, is_default BOOL, updated_at TIMESTAMP, created_at TIMESTAMP) OPTIONS(description="ユーザー設定情報。個人設定、表示設定、通知設定を管理。");
CREATE OR REPLACE TABLE `tt_hackathon.integration_logs` (log_id STRING, integration_name STRING, direction STRING, message_type STRING, payload_size_bytes INT64, status STRING, error_message STRING, timestamp TIMESTAMP) OPTIONS(labels=[("data_type", "integration"), ("monitoring", "enabled")]);
CREATE OR REPLACE TABLE `tt_hackathon.cache_statistics` (stat_id STRING, cache_name STRING, hit_count INT64, miss_count INT64, eviction_count INT64, memory_usage_mb NUMERIC, timestamp TIMESTAMP, date_partition DATE) OPTIONS(description="キャッシュ統計情報。ヒット率、メモリ使用量、エビクション回数を記録。");
CREATE OR REPLACE TABLE `tt_hackathon.feature_flags` (flag_id STRING, flag_name STRING, description STRING, is_enabled BOOL, target_percentage NUMERIC, created_by STRING, created_at TIMESTAMP, updated_at TIMESTAMP) OPTIONS(labels=[("data_type", "config"), ("feature_management", "true")]);
CREATE OR REPLACE TABLE `tt_hackathon.email_campaigns` (campaign_id STRING, subject STRING, sender_email STRING, recipient_count INT64, sent_count INT64, opened_count INT64, clicked_count INT64, bounced_count INT64, sent_at TIMESTAMP) OPTIONS(description="メールキャンペーン実績。送信数、開封率、クリック率、バウンス率を記録。");
CREATE OR REPLACE TABLE `tt_hackathon.geo_locations` (location_id STRING, country STRING, region STRING, city STRING, latitude NUMERIC, longitude NUMERIC, timezone STRING, population INT64) OPTIONS(labels=[("data_type", "reference"), ("geographic", "true")]);
CREATE OR REPLACE TABLE `tt_hackathon.currency_rates` (rate_id STRING, base_currency STRING, target_currency STRING, exchange_rate NUMERIC, rate_date DATE, source STRING, created_at TIMESTAMP, updated_at TIMESTAMP) OPTIONS(description="為替レート情報。通貨換算に使用する日次レートデータ。");
CREATE OR REPLACE TABLE `tt_hackathon.ml_model_predictions` (prediction_id STRING, model_name STRING, input_data JSON, prediction_result JSON, confidence_score NUMERIC, model_version STRING, predicted_at TIMESTAMP) OPTIONS(description="機械学習モデル予測結果。予測値、信頼度スコア、モデルバージョンを記録。", labels=[("data_type", "ml_output")]);
CREATE OR REPLACE TABLE `tt_hackathon.social_media_mentions` (mention_id STRING, platform STRING, username STRING, content STRING, sentiment STRING, engagement_count INT64, posted_at TIMESTAMP, collected_at TIMESTAMP) OPTIONS(labels=[("data_type", "social_media"), ("sentiment_analysis", "enabled")]);
CREATE OR REPLACE TABLE `tt_hackathon.iot_sensor_data` (sensor_id STRING, device_id STRING, sensor_type STRING, measurement_value NUMERIC, unit STRING, location STRING, timestamp TIMESTAMP, battery_level NUMERIC) OPTIONS(description="IoTセンサーデータ。温度、湿度、位置情報等のセンサー測定値を記録。");
CREATE OR REPLACE TABLE `tt_hackathon.compliance_reports` (report_id STRING, regulation_type STRING, compliance_status STRING, findings JSON, risk_level STRING, auditor STRING, report_date DATE, next_review_date DATE) OPTIONS(labels=[("data_type", "compliance"), ("confidential", "true")]);
CREATE OR REPLACE TABLE `tt_hackathon.subscription_plans` (plan_id STRING, plan_name STRING, description STRING, price NUMERIC, billing_cycle STRING, features JSON, is_active BOOL, created_at TIMESTAMP) OPTIONS(description="サブスクリプションプラン情報。料金体系、機能、課金サイクルを管理。");
CREATE OR REPLACE TABLE `tt_hackathon.customer_support_tickets` (ticket_id STRING, customer_id STRING, subject STRING, description STRING, priority STRING, status STRING, assigned_to STRING, created_at TIMESTAMP, resolved_at TIMESTAMP) OPTIONS(labels=[("data_type", "support"), ("sla_tracking", "enabled")]);
CREATE OR REPLACE TABLE `tt_hackathon.inventory_forecasts` (forecast_id STRING, product_id STRING, forecast_period STRING, predicted_demand INT64, confidence_interval JSON, model_accuracy NUMERIC, generated_at TIMESTAMP) OPTIONS(description="在庫需要予測。機械学習による需要予測と精度指標を記録。");
CREATE OR REPLACE TABLE `tt_hackathon.network_traffic_logs` (log_id STRING, source_ip STRING, destination_ip STRING, port INT64, protocol STRING, bytes_transferred INT64, duration_ms INT64, timestamp TIMESTAMP) OPTIONS(labels=[("data_type", "network"), ("security_monitoring", "enabled")]);
CREATE OR REPLACE TABLE `tt_hackathon.ab_test_results` (test_id STRING, experiment_name STRING, variant STRING, user_id STRING, conversion_event STRING, timestamp TIMESTAMP, session_id STRING) OPTIONS(description="A/Bテスト結果。実験バリアント、コンバージョンイベント、ユーザー行動を記録。");
CREATE OR REPLACE TABLE `tt_hackathon.data_lineage_tracking` (lineage_id STRING, source_table STRING, target_table STRING, transformation_type STRING, dependency_level INT64, last_updated TIMESTAMP, created_by STRING) OPTIONS(labels=[("data_type", "metadata"), ("governance", "critical")]);
CREATE OR REPLACE TABLE `tt_hackathon.real_time_alerts` (alert_id STRING, alert_type STRING, severity STRING, message STRING, affected_system STRING, triggered_at TIMESTAMP, acknowledged_at TIMESTAMP, resolved_at TIMESTAMP) OPTIONS(description="リアルタイムアラート。システム異常、しきい値超過、エラー発生を記録。");
CREATE OR REPLACE TABLE `tt_hackathon.customer_journey_events` (event_id STRING, customer_id STRING, touchpoint STRING, event_type STRING, channel STRING, campaign_id STRING, timestamp TIMESTAMP, session_id STRING) OPTIONS(labels=[("data_type", "journey"), ("analytics", "enabled")]);
CREATE OR REPLACE TABLE `tt_hackathon.price_optimization_data` (optimization_id STRING, product_id STRING, current_price NUMERIC, suggested_price NUMERIC, demand_elasticity NUMERIC, competitor_price NUMERIC, optimization_date DATE) OPTIONS(description="価格最適化データ。需要弾力性、競合価格、推奨価格を記録。");
CREATE OR REPLACE TABLE `tt_hackathon.regulatory_changes` (change_id STRING, regulation_name STRING, change_description STRING, effective_date DATE, impact_assessment STRING, compliance_actions JSON, status STRING) OPTIONS(labels=[("data_type", "regulatory"), ("compliance_tracking", "required")]);
CREATE OR REPLACE TABLE `tt_hackathon.data_retention_policies` (policy_id STRING, table_name STRING, retention_period_days INT64, archive_location STRING, deletion_criteria JSON, last_applied TIMESTAMP, created_by STRING) OPTIONS(description="データ保持ポリシー。テーブル別の保持期間、アーカイブ場所、削除条件を管理。", labels=[("data_type", "policy")]);
CREATE OR REPLACE TABLE `tt_hackathon.blockchain_transactions` (transaction_hash STRING, block_number INT64, from_address STRING, to_address STRING, value NUMERIC, gas_used INT64, timestamp TIMESTAMP) OPTIONS(labels=[("data_type", "blockchain")]);
CREATE OR REPLACE TABLE `tt_hackathon.weather_data` (weather_id STRING, location STRING, temperature NUMERIC, humidity NUMERIC, pressure NUMERIC, wind_speed NUMERIC, timestamp TIMESTAMP) OPTIONS(description="気象データ。温度、湿度、気圧、風速の観測値を記録。");
CREATE OR REPLACE TABLE `tt_hackathon.energy_consumption` (meter_id STRING, building_id STRING, consumption_kwh NUMERIC, cost NUMERIC, timestamp TIMESTAMP, meter_type STRING) OPTIONS(labels=[("data_type", "energy"), ("sustainability", "tracking")]);
CREATE OR REPLACE TABLE `tt_hackathon.document_versions` (document_id STRING, version_number INT64, author STRING, changes_summary STRING, file_path STRING, created_at TIMESTAMP) OPTIONS(description="文書バージョン管理。文書の変更履歴、作成者、変更内容を記録。");
CREATE OR REPLACE TABLE `tt_hackathon.quality_control_tests` (test_id STRING, product_batch STRING, test_type STRING, result STRING, inspector STRING, tested_at TIMESTAMP) OPTIONS(labels=[("data_type", "quality"), ("manufacturing", "critical")]);
CREATE OR REPLACE TABLE `tt_hackathon.mobile_app_events` (event_id STRING, user_id STRING, app_version STRING, event_name STRING, properties JSON, timestamp TIMESTAMP) OPTIONS(description="モバイルアプリイベント。ユーザー行動、アプリバージョン、イベントプロパティを記録。");
CREATE OR REPLACE TABLE `tt_hackathon.competitor_analysis` (analysis_id STRING, competitor_name STRING, metric_type STRING, metric_value NUMERIC, analysis_date DATE, source STRING) OPTIONS(labels=[("data_type", "competitive"), ("business_intelligence", "enabled")]);
CREATE OR REPLACE TABLE `tt_hackathon.training_records` (training_id STRING, employee_id STRING, course_name STRING, completion_status STRING, score NUMERIC, completed_at TIMESTAMP) OPTIONS(description="研修記録。従業員の研修受講履歴、完了状況、成績を管理。");
CREATE OR REPLACE TABLE `tt_hackathon.vendor_evaluations` (evaluation_id STRING, vendor_id STRING, evaluation_criteria JSON, overall_score NUMERIC, evaluator STRING, evaluation_date DATE) OPTIONS(labels=[("data_type", "vendor_management"), ("procurement", "critical")]);
CREATE OR REPLACE TABLE `tt_hackathon.sustainability_metrics` (metric_id STRING, category STRING, metric_name STRING, value NUMERIC, unit STRING, reporting_period STRING, timestamp TIMESTAMP) OPTIONS(description="持続可能性指標。環境負荷、エネルギー効率、廃棄物削減等のESG指標を記録。", labels=[("data_type", "sustainability"), ("esg_reporting", "required")]);

-- 全テーブルのダミーデータ挿入（効率化実装）
INSERT INTO `tt_hackathon.system_metrics` SELECT CONCAT('MET', LPAD(CAST(seq AS STRING), 6, '0')), 'web-server', 'cpu_usage', CAST(MOD(seq, 100) AS NUMERIC), 'percent', CURRENT_TIMESTAMP(), CONCAT('host-', CAST(seq AS STRING)), 'prod' FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.notification_history` SELECT CONCAT('NOT', LPAD(CAST(seq AS STRING), 6, '0')), CONCAT('USER', CAST(seq AS STRING)), 'order', 'Order Update', 'Your order has been shipped', 'email', 'sent', CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.api_usage_logs` SELECT CONCAT('API', LPAD(CAST(seq AS STRING), 6, '0')), CONCAT('KEY', CAST(seq AS STRING)), '/api/users', 'GET', 200, 150 + seq, 1024 + seq, CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.backup_records` SELECT CONCAT('BKP', LPAD(CAST(seq AS STRING), 6, '0')), 'customers', 'full', CONCAT('/backups/', CAST(seq AS STRING), '.sql'), CAST((1.0 + seq) AS NUMERIC), 'completed', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.security_events` SELECT CONCAT('SEC', LPAD(CAST(seq AS STRING), 6, '0')), CONCAT('USER', CAST(seq AS STRING)), 'login_failed', 'medium', 'Failed login attempt', '192.168.1.1', 'Mozilla/5.0', CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.performance_metrics` SELECT CONCAT('PERF', LPAD(CAST(seq AS STRING), 6, '0')), CONCAT('QRY', CAST(seq AS STRING)), 100 + seq, 1000 + seq, 1024 + seq, CAST((10.0 + seq) AS NUMERIC), CAST((512.0 + seq) AS NUMERIC), CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.data_quality_checks` SELECT CONCAT('QC', LPAD(CAST(seq AS STRING), 6, '0')), 'customers', 'email', 'not_null', 'not null', 'not null', 'passed', CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.user_preferences` SELECT CONCAT('PREF', LPAD(CAST(seq AS STRING), 6, '0')), CONCAT('USER', CAST(seq AS STRING)), 'display', 'theme', 'dark', false, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.integration_logs` SELECT CONCAT('INT', LPAD(CAST(seq AS STRING), 6, '0')), 'salesforce', 'inbound', 'customer', 1024 + seq, 'success', NULL, CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.cache_statistics` SELECT CONCAT('CACHE', LPAD(CAST(seq AS STRING), 6, '0')), 'redis_main', 1000 + seq, 100 + seq, 10 + seq, CAST((128.0 + seq) AS NUMERIC), CURRENT_TIMESTAMP(), CURRENT_DATE() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.feature_flags` SELECT CONCAT('FLAG', LPAD(CAST(seq AS STRING), 6, '0')), CONCAT('feature_', CAST(seq AS STRING)), 'Feature description', true, CAST(100.0 AS NUMERIC), 'admin', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.email_campaigns` SELECT CONCAT('EMAIL', LPAD(CAST(seq AS STRING), 6, '0')), 'Campaign Subject', 'noreply@example.com', 1000 + seq, 950 + seq, 200 + seq, 50 + seq, 5 + seq, CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.geo_locations` SELECT CONCAT('GEO', LPAD(CAST(seq AS STRING), 6, '0')), 'Japan', 'Tokyo', 'Shibuya', CAST(35.0 AS NUMERIC), CAST(139.0 AS NUMERIC), 'Asia/Tokyo', 100000 + seq FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.currency_rates` SELECT CONCAT('RATE', LPAD(CAST(seq AS STRING), 6, '0')), 'JPY', 'USD', CAST(0.007 AS NUMERIC), CURRENT_DATE(), 'bank_api', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.ml_model_predictions` SELECT CONCAT('ML', LPAD(CAST(seq AS STRING), 6, '0')), 'churn_prediction', JSON '{"feature1": 0.5}', JSON '{"prediction": 0.75}', CAST(0.85 AS NUMERIC), 'v1.2.3', CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.social_media_mentions` SELECT CONCAT('SM', LPAD(CAST(seq AS STRING), 6, '0')), 'Twitter', CONCAT('user', CAST(seq AS STRING)), 'Great product!', 'positive', seq, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.iot_sensor_data` SELECT CONCAT('IOT', LPAD(CAST(seq AS STRING), 6, '0')), CONCAT('DEV', CAST(seq AS STRING)), 'temperature', CAST((20.0 + seq) AS NUMERIC), 'celsius', 'Building A', CURRENT_TIMESTAMP(), CAST(80.0 AS NUMERIC) FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.compliance_reports` SELECT CONCAT('COMP', LPAD(CAST(seq AS STRING), 6, '0')), 'GDPR', 'compliant', JSON '{"findings": []}', 'low', 'auditor1', CURRENT_DATE(), DATE_ADD(CURRENT_DATE(), INTERVAL 365 DAY) FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.subscription_plans` SELECT CONCAT('PLAN', LPAD(CAST(seq AS STRING), 6, '0')), CONCAT('Plan ', CAST(seq AS STRING)), 'Plan description', CAST((1000 + seq) AS NUMERIC), 'monthly', JSON '{"features": []}', true, CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.customer_support_tickets` SELECT CONCAT('TKT', LPAD(CAST(seq AS STRING), 6, '0')), CONCAT('CUST', CAST(seq AS STRING)), 'Issue subject', 'Issue description', 'medium', 'open', 'agent1', CURRENT_TIMESTAMP(), NULL FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.inventory_forecasts` SELECT CONCAT('FCST', LPAD(CAST(seq AS STRING), 6, '0')), CONCAT('PROD', CAST(seq AS STRING)), 'monthly', 100 + seq, JSON '{"lower": 90, "upper": 110}', CAST(0.85 AS NUMERIC), CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.network_traffic_logs` SELECT CONCAT('NET', LPAD(CAST(seq AS STRING), 6, '0')), '192.168.1.1', '192.168.1.100', 80, 'HTTP', 1024 + seq, 100 + seq, CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.ab_test_results` SELECT CONCAT('AB', LPAD(CAST(seq AS STRING), 6, '0')), 'test_checkout', 'variant_a', CONCAT('USER', CAST(seq AS STRING)), 'purchase', CURRENT_TIMESTAMP(), CONCAT('SESS', CAST(seq AS STRING)) FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.data_lineage_tracking` SELECT CONCAT('LIN', LPAD(CAST(seq AS STRING), 6, '0')), 'raw_customers', 'customer_profiles', 'transformation', 1, CURRENT_TIMESTAMP(), 'system' FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.real_time_alerts` SELECT CONCAT('ALT', LPAD(CAST(seq AS STRING), 6, '0')), 'system', 'high', 'Alert message', 'web_server', CURRENT_TIMESTAMP(), NULL, NULL FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.customer_journey_events` SELECT CONCAT('JRN', LPAD(CAST(seq AS STRING), 6, '0')), CONCAT('CUST', CAST(seq AS STRING)), 'website', 'page_view', 'web', 'CAMP001', CURRENT_TIMESTAMP(), CONCAT('SESS', CAST(seq AS STRING)) FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.price_optimization_data` SELECT CONCAT('PRC', LPAD(CAST(seq AS STRING), 6, '0')), CONCAT('PROD', CAST(seq AS STRING)), CAST((1000 + seq) AS NUMERIC), CAST((1100 + seq) AS NUMERIC), CAST(1.2 AS NUMERIC), CAST((1050 + seq) AS NUMERIC), CURRENT_DATE() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.regulatory_changes` SELECT CONCAT('REG', LPAD(CAST(seq AS STRING), 6, '0')), 'Data Protection Act', 'New privacy requirements', DATE_ADD(CURRENT_DATE(), INTERVAL 30 DAY), 'medium', JSON '{"actions": []}', 'pending' FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.data_retention_policies` SELECT CONCAT('RET', LPAD(CAST(seq AS STRING), 6, '0')), 'customers', 2555, '/archive/customers', JSON '{"criteria": "inactive"}', CURRENT_TIMESTAMP(), 'admin' FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.blockchain_transactions` SELECT CONCAT('0x', LPAD(CAST(seq AS STRING), 8, '0')), seq, CONCAT('0xabc', CAST(seq AS STRING)), CONCAT('0xdef', CAST(seq AS STRING)), CAST(seq AS NUMERIC), 21000 + seq, CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.weather_data` SELECT CONCAT('WTH', LPAD(CAST(seq AS STRING), 6, '0')), 'Tokyo', CAST((15.0 + seq) AS NUMERIC), CAST((40.0 + seq) AS NUMERIC), CAST((1000.0 + seq) AS NUMERIC), CAST(seq AS NUMERIC), CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.energy_consumption` SELECT CONCAT('MTR', LPAD(CAST(seq AS STRING), 6, '0')), CONCAT('BLD', CAST(seq AS STRING)), CAST((100.0 + seq) AS NUMERIC), CAST((seq * 0.25) AS NUMERIC), CURRENT_TIMESTAMP(), 'electric' FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.document_versions` SELECT CONCAT('DOC', LPAD(CAST(seq AS STRING), 6, '0')), 1 + MOD(seq, 5), 'author1', 'Updated content', '/docs/file.pdf', CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.quality_control_tests` SELECT CONCAT('QCT', LPAD(CAST(seq AS STRING), 6, '0')), CONCAT('BATCH', CAST(seq AS STRING)), 'durability', 'passed', 'inspector1', CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.mobile_app_events` SELECT CONCAT('APP', LPAD(CAST(seq AS STRING), 6, '0')), CONCAT('USER', CAST(seq AS STRING)), '1.2.3', 'button_click', JSON '{"button": "purchase"}', CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.competitor_analysis` SELECT CONCAT('CMP', LPAD(CAST(seq AS STRING), 6, '0')), 'Competitor A', 'market_share', CAST((10.0 + seq) AS NUMERIC), CURRENT_DATE(), 'market_research' FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.training_records` SELECT CONCAT('TRN', LPAD(CAST(seq AS STRING), 6, '0')), CONCAT('EMP', CAST(seq AS STRING)), 'Safety Training', 'completed', CAST((70.0 + seq) AS NUMERIC), CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.vendor_evaluations` SELECT CONCAT('VND', LPAD(CAST(seq AS STRING), 6, '0')), CONCAT('SUP', CAST(seq AS STRING)), JSON '{"quality": 4, "delivery": 5}', CAST((3.0 + seq * 0.1) AS NUMERIC), 'manager1', CURRENT_DATE() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;
INSERT INTO `tt_hackathon.sustainability_metrics` SELECT CONCAT('SUS', LPAD(CAST(seq AS STRING), 6, '0')), 'energy', 'carbon_footprint', CAST((1000.0 + seq) AS NUMERIC), 'kg_co2', '2025-Q1', CURRENT_TIMESTAMP() FROM UNNEST(GENERATE_ARRAY(1, 1000)) as seq;

-- =============================================================================
-- 完了サマリー
-- =============================================================================
-- 合計60テーブル作成完了:
-- - 既存10テーブル（1000件のダミーデータに更新）
-- - 新規50テーブル（各1000件のダミーデータ）
--
-- 各テーブルの特徴:
-- - 多様なデータ型（STRING, NUMERIC, TIMESTAMP, JSON, BOOL等）
-- - 様々なメタデータパターン（説明あり/なし、ラベルあり/なし）
-- - データガバナンステストに適した多様性
-- - 上流・下流・中間テーブルの依存関係
-- - NULLデータを含む品質テストパターン
-- =============================================================================
