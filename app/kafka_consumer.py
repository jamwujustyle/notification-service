from aiokafka import AIOKafkaConsumer
import json
import os
import asyncio
from .email_service import EmailService
from .handlers import handle_user_registered_event
from .configs.logging_config import logger


async def start_kafka_consumer():
    try:
        consumer = AIOKafkaConsumer(
            "user-registered",
            bootstrap_servers=os.environ.get(
                "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
            ),
            group_id="notification-service",
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )

        await consumer.start()
        logger.critical(
            f'Kakfa consumer started, connected to {os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")}'
        )

        try:
            async for message in consumer:
                event_data = message.value

                if event_data.get("event_type") == "user_registered":
                    await handle_user_registered_event(event_data)
        except Exception as ex:
            logger.debug(f"Error in Kafka consumer: {ex}")
        finally:
            await consumer.stop()
    except Exception as ex:
        logger.critical(f"Failed to start Kafka consumer: {ex}")
        await asyncio.sleep(10)
