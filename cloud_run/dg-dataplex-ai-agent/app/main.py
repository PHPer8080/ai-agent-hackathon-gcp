import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.core import globals as g
from app.core.config import AgentConfig
from app.services.initialization_service import InitializationService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Google ADK初期化：起動時1回のみ実行"""
    logger.info("DG Dataplex AI Agent起動中...")

    # 設定とサービス初期化
    config = AgentConfig()
    initialization_service = InitializationService()
    (g.agent, g.runner, g.session_service) = initialization_service.initialize_all(config.APP_NAME)

    yield


app = FastAPI(title="DG Dataplex AI Agent", description="Google Cloud Dataplex専用AIエージェント - データ品質ルール提案", version="1.0.0", docs_url="/docs", redoc_url="/redoc", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    # FIXME: 本番環境では許可するオリジンを制限する
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIルーター登録
app.include_router(health_router)
app.include_router(chat_router)
