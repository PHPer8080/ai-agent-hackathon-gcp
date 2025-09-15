#!/bin/bash
set -e

# 変数の設定
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_ID=$1
SERVICE_ACCOUNT=$2

SERVICE_NAME="dg-data-governance-chatui"
REGION="asia-northeast1"
IMAGE_REPOSITORY="${REGION}-docker.pkg.dev/${PROJECT_ID}/cloud-run-source-deploy"

# 依存サービスの内部エンドポイント（describe取得）
AGENT_URL=$(gcloud run services describe dg-data-governance-agent --platform managed --region "${REGION}" --project="${PROJECT_ID}" --format 'value(status.url)' 2>/dev/null || echo "")

# スクリプトのディレクトリに移動
cd "${SCRIPT_DIR}"

# Docker認証の設定
echo "Docker認証設定中..."
gcloud auth configure-docker "${REGION}-docker.pkg.dev" --quiet

echo "イメージビルド中: ${IMAGE_REPOSITORY}/${SERVICE_NAME}:latest"
docker build -t ${SERVICE_NAME}:latest -f "${SCRIPT_DIR}/Dockerfile" "${SCRIPT_DIR}" \
&& docker tag ${SERVICE_NAME}:latest "${IMAGE_REPOSITORY}/${SERVICE_NAME}:latest" \
&& echo "イメージプッシュ中..." \
&& docker push "${IMAGE_REPOSITORY}/${SERVICE_NAME}:latest"

gcloud run deploy ${SERVICE_NAME} \
--image "${IMAGE_REPOSITORY}/${SERVICE_NAME}:latest" \
--platform managed \
--region "${REGION}" \
--port=8000 \
--service-account="${SERVICE_ACCOUNT}" \
--ingress=all \
--no-allow-unauthenticated \
--set-env-vars="AGENT_URL=${AGENT_URL}" \
--project="${PROJECT_ID}"

echo "✅ ${SERVICE_NAME} deployed successfully!"
