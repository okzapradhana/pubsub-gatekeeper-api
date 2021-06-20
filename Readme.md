# Gatekeeper API with Google PubSub
## About
Realtime data transport from Backend Team that sends JSON payload to BigQuery as the database. Those payloads **MUST** pass the gatekeeper's schema rule in order to can be processed to Database.


## Tech Stack:
1. Python
2. Flask
3. Google PubSub

## Setup
### Python
1. Create your python virtual environment
   ```
   python -m venv venv
   ```
2. Activate the environment
   ```
   source venv/bin/activate
   ```
3. Install the depedencies
   ```
   pip install -r requirements.txt
   ```

### Google Cloud
1. Install [gcloud](https://cloud.google.com/sdk/docs/quickstart) if you haven't installed it yet.
2. Simply run the bash script named `pubsub.sh` to create the topic and subscriber which will subscribe/listen to created topic/
   ```
   ./pubsub.sh
   ```
3. Be sure that you **MUST** [create/download your Service Account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) because that needed by `GOOGLE_APPLICATION_CREDENTIALS` variable at `services/` folder.

## How To Use
1. Run the flask APP by:
   ```
   FLASK_APP=app/main.py FLASK_ENV=development flask run --port <port>
   ```
   If you are in development phase, and want to auto reload every changes you made to the code.
   But if you are in production. Use:
   ```
   FLASK_APP=app/main.py FLASK_ENV=production flask run --port <port>
   ```
   You can specify the port based on your need, for example `8080`
2. Open your other terminal. Then run the **subscriber** to listen and fetch every message sent to **topic** by the **publisher** by executing:
   ```
   python services/subscriber.py
   ```

## Testing
   To perform functional testing on this project. Simply run:
   ```
   pytest
   ```