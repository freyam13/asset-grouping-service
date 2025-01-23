import logging

from fastapi import FastAPI

from src.api.routes import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Tamnoon Asset Service",
    description="Service for presisting and grouping assets based on user-defined rules.",
    version="1.0.0",
)

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    logger.info("Starting Tamnoon Asset Service ...")
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
