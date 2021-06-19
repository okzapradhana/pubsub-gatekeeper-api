from google.api_core.exceptions import BadRequest, GoogleAPIError
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from bigquery import BigQueryClient
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
    bq = BigQueryClient()

    for activity in transactions['activities']:
        try:
            table = activity['table']
            if activity['operation'] == 'insert':
                values = activity['col_values']
                bq.insert(
                    table,
                    values,
                    column_names=activity['col_names'], column_types=activity['col_types'])
            elif activity['operation'] == 'delete':
                values = activity['value_to_delete']['col_values']
                bq.delete(
                    table,
                    values,
                    column_names=activity['value_to_delete']['col_names'],
                    column_types=activity['value_to_delete']['col_types'])
        except BadRequest as error:
            print(f"Bad Request {error.code}: {error.message}")
        except GoogleAPIError as error:
            print(f"GoogleAPIError: {error}")
        except Exception as error:
            print(f"Exception at: {error}")
        except TypeError as error:
            print(f"Type error at: {error}")
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
