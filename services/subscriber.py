from google.api_core.exceptions import BadRequest, GoogleAPIError
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from dotenv import load_dotenv
from pubsub import PubSubClient
from bigquery_client import BigQueryClient
import json
import os
import logging
sub = pubsub_v1.SubscriberClient()
load_dotenv()

os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
PROJECT_ID = os.getenv('PROJECT_ID')
DATASET_ID = os.getenv('DATASET_ID')
SUBSCRIPTION_ID = os.getenv('SUBSCRIPTION_ID')

client = PubSubClient(PROJECT_ID, SUBSCRIPTION_ID)
bq = BigQueryClient(PROJECT_ID, DATASET_ID)


def callback(message):
    logging.warning(f"Received message: \n {message}")

    transactions = json.loads(message.data.decode('utf-8'))

    for activity in transactions['activities']:
        try:
            bq.process(activity)
        except BadRequest as error:
            logging.error(f"BadRequest {error.code}: {error.message}")
            bq.rollback()
        except GoogleAPIError as error:
            logging.error(f"GoogleAPIError: {error}")
            bq.rollback()
        except ValueError as error:
            logging.error(f"ValueError: {error}")
            bq.rollback()
        except TypeError as error:
            logging.error(f"TypeError: {error}")
            bq.rollback()
        except Exception as error:
            logging.error(f"Exception: {error}")
            bq.rollback()

    bq.execute()
    message.ack()

    logging.warning(f'Message {transactions} has been acknowledged!')


streaming_pull = client._subscribe(callback=callback)
logging.warning(f"Listening message... \n")

with sub:
    try:
        streaming_pull.result()
    except TimeoutError:
        streaming_pull.cancel()
        streaming_pull.result()
