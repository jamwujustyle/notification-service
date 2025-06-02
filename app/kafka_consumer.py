from aiokafka import AIOKafkaConsumer
import json
import os
import asyncio
from .email_service import EmailService
from .handlers import handle_user_registered_event


async def start_kafka_consumer():
    consumer = AIOKafkaConsumer(
        "user-registered",
        bootstrap_servers=os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
        group_id="notification-service",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    await consumer.start()

    try:
        async for message in consumer:
            event_data = message.value

            if event_data.get("event_type") == "user-registeted":
                await handle_user_registered_event(event_data)
    except Exception as ex:
        print(f"Error in Kafka consumer: {ex}")
    finally:
        await consumer.stop()
