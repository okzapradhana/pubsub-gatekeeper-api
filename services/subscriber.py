from google.api_core.exceptions import BadRequest, GoogleAPIError
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
import bigquery_client
import json
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/chapmon/bootcamps/blank-space-de-batch1/week-4/script/keyfile.json'

sub = pubsub_v1.SubscriberClient()
PROJECT_ID = 'static-gravity-312212'
SUBSCRIPTION_ID = 'db-sub'
TIMEOUT = 10
subscription_path = sub.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)


def callback(message):
    print("message: ", message)
    transactions = json.loads(message.data.decode('utf-8'))
    try:
        bigquery_client.process(transactions)
    except BadRequest as error:
        print(f"Bad Request {error.code}: {error.message}")
    except GoogleAPIError as error:
        print(f"GoogleAPIError: {error}")
    except ValueError as error:
        print(f"Value Error: {error}")
    except TypeError as error:
        print(f"Type Error: {error}")
    except Exception as error:
        print(f"Exception message: {error}")
    message.ack()
    print(f'Message {message} has been acknowledged')


streaming_pull = sub.subscribe(subscription_path, callback=callback)
print(f"Listening message on {subscription_path}... \n")

with sub:
    try:
        streaming_pull.result()
    except TimeoutError:
        streaming_pull.cancel()
        streaming_pull.result()
