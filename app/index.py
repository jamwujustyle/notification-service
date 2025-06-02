from fastapi import FastAPI
import asyncio
from contextlib import asynccontextmanager
from .kafka_consumer import start_kafka_consumer
from .email_service import EmailService
from .configs.logging_config import logger


kafka_consumer_task = None


@asynccontextmanager
async def lifespan(app: FastAPI):

    global kafka_consumer_task
    kafka_consumer_task = asyncio.create_task(start_kafka_consumer())
    yield

    if kafka_consumer_task:
        kafka_consumer_task.cancel()
        try:
            await kafka_consumer_task
        except asyncio.CancelledError:
            pass


app = FastAPI(title="Notification Service", lifespan=lifespan)

email_service = EmailService()


@app.get("/health")
async def health_check():
    logger.critical("hello world")
    return {"status": "healthy"}
