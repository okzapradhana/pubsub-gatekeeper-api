from google.cloud import pubsub_v1
from dotenv import load_dotenv
import os
import logging
load_dotenv()
os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

pub = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv('PROJECT_ID')
TOPIC_ID = os.getenv('TOPIC_ID')
topic_path = pub.topic_path(PROJECT_ID, TOPIC_ID)


def push(message):
    future = pub.publish(topic_path, message)
    return future.result()


logging.info(f"Published messages to {topic_path}")
