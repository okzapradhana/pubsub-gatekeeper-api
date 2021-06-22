from dotenv import load_dotenv
from services.pubsub import PubSubClient
import os
import logging

load_dotenv()

os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

PROJECT_ID = os.getenv('PROJECT_ID')
TOPIC_ID = os.getenv('TOPIC_ID')

client = PubSubClient(PROJECT_ID, TOPIC_ID)


def push(message):
    future = client._publish(message)
    return future.result()


logging.info(f"Message has been published")
