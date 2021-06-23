# Gatekeeper API with Google PubSub
## About
API endpoint to validate and process incoming message that comes from Backend Team to our Database. 

Those payloads **MUST** pass the gatekeeper's schema rule (specified in `validator/schema.py`) in order to can be processed to Database.

It is similar to CDC process that empowers message queue with help from Google PubSub. 

## Tech Stack:
1. Python
2. Flask
3. Google PubSub
4. Google BigQuery

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
### Prometheus Pushgateway
Prometheus pushgateway allows batch jobs to expose their metrics to Prometheus. Such as how many specific endpoint got hit, how many valid and invalid payload request that sent to the endpoint, etc. You can read more on [docs here](https://github.com/prometheus/pushgateway)

First of all, you need to pull the image from [DockerHub](https://hub.docker.com/r/prom/pushgateway)

Then, how to run the pulled image? I included those steps on [How To Use](#how-to-use)
```
docker pull prom/pushgateway
```

### Environment Variables
Create `.env` on root of your project directory that corresponds to `.env.example` in this repository which are:
```
GOOGLE_APPLICATION_CREDENTIALS=
PROJECT_ID=
DATASET_ID=
TOPIC_ID=
SUBSCRIPTION_ID=
PUSHGATEWAY_PROMETHEUS_HOST=
```
**Note:**<br>
Points your `GOOGLE_APPLICATION_CREDENTIALS` to your service account file path.

### Google Cloud
1. Install [gcloud](https://cloud.google.com/sdk/docs/quickstart) if you haven't installed it yet.
2. Simply run the bash script named `pubsub.sh` to create the topic and subscriber which will subscribe/listen to created topic/
   ```
   ./pubsub.sh
   ```
3. Be sure that you **MUST** [create/download your Service Account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) and points your `GOOGLE_APPLICATION_CREDENTIALS` to the downloaded service account path.

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
3. Run the docker image by:
   ```
   docker run -d -p 9091:9091 prom/pushgateway
   ```
   If the container is running as expected, you can access `localhost:9091` using your browser.

   Then, fill the `PUSHGATEWAY_PROMETHEUS_HOST` variable with `localhost:9091` , you don't have to set `9091` as the port. You can change the port when running the image based on your needs.

## Pushgateway Metrics Result

1. How many valid payload that has been sent by hitting our API ?
![valid-schema-count](images/Valid%20Payload%20Schema%20Metrics.png)

2. How many invalid payload that has been sent by hitting our API ?
![invalid-schema-count](images/Invalid%20Payload%20Schema%20Metrics.png)

   As this two examples are not enough, this one is included in what can/should I improve on this project. 
## Testing
  ### Functional Test
   To perform functional testing on this project. Simply run:
   ```
   pytest
   ```
  ### Load Test
  This project is using locust to perform performance test. To run this, open your terminal and execute this command:
  ```
  locust
  ```
  Then go to http://localhost:8089 and set
  1. Max users
  2. Spawn user per second
  3. Host 
  
  Locust tutorial: https://docs.locust.io/en/stable/what-is-locust.html