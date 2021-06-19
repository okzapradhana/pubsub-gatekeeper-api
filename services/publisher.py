from google.cloud import pubsub_v1
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/chapmon/bootcamps/blank-space-de-batch1/week-4/script/keyfile.json'

pub = pubsub_v1.PublisherClient()
PROJECT_ID = 'static-gravity-312212'
TOPIC_ID = 'db-transaction-topic'
topic_path = pub.topic_path(PROJECT_ID, TOPIC_ID)


def push(message):
    future = pub.publish(topic_path, message)
    return future.result()


print(f"Published messages to {topic_path}")
