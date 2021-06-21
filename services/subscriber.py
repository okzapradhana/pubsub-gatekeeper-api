from google.api_core.exceptions import BadRequest, GoogleAPIError
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from dotenv import load_dotenv
from pubsub import PubSubClient
import bigquery_client
import json
import os
import logging
sub = pubsub_v1.SubscriberClient()
load_dotenv()

os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
PROJECT_ID = os.getenv('PROJECT_ID')
SUBSCRIPTION_ID = os.getenv('SUBSCRIPTION_ID')
client = PubSubClient(PROJECT_ID, SUBSCRIPTION_ID)


def callback(message):
    logging.info(f"Received message: \n {message}")

    transactions = json.loads(message.data.decode('utf-8'))
    try:
        bigquery_client.process(transactions)
    except BadRequest as error:
        logging.error(f"Bad Request {error.code}: {error.message}")
    except GoogleAPIError as error:
        logging.error(f"GoogleAPIError: {error}")
    except ValueError as error:
        logging.error(f"Value Error: {error}")
    except TypeError as error:
        logging.error(f"Type Error: {error}")
    except Exception as error:
        logging.error(f"Exception message: {error}")

    message.ack()
    logging.info(f'Message {message} has been acknowledged!')


streaming_pull = client._subscribe(callback=callback)
logging.info(f"Listening message... \n")

with sub:
    try:
        streaming_pull.result()
    except TimeoutError:
        streaming_pull.cancel()
        streaming_pull.result()
