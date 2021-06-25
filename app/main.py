from flask import Flask, request, jsonify, Response
from google.api_core.exceptions import BadRequest
from prometheus_client.registry import CollectorRegistry
from validator.main import validate_payload
from http import HTTPStatus
from dotenv import load_dotenv
from prometheus_client import Summary, Counter, Histogram, Gauge, push_to_gateway
import wtforms
import os

load_dotenv()
os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
PUSHGATEWAY_PROMETHEUS_HOST = os.getenv('PUSHGATEWAY_PROMETHEUS_HOST')

app = Flask(__name__)
registry = CollectorRegistry()
invalid_payload_counter = Counter('invalid_payload_count',
                                  'The total number of invalid payload request that hit /api/activities', registry=registry)

valid_payload_registry = CollectorRegistry()
valid_payload_counter = Counter('valid_payload_count',
                                'The total number of payload request that hit /api/activities', registry=valid_payload_registry)


@app.route("/")
def say_hello():
    base_registry = CollectorRegistry()
    g = Gauge('job_last_success_unixtime',
              'Last time a batch job successfully finished', registry=base_registry)
    g.set_to_current_time()
    push_to_gateway(PUSHGATEWAY_PROMETHEUS_HOST,
                    job='base_endpoint', registry=base_registry)
    return "Hello World, congratulations on installing Flask"


@app.route("/api/activities", methods=["POST"])
def handler():
    validate_payload(request)
    valid_payload_counter.inc()
    push_to_gateway(PUSHGATEWAY_PROMETHEUS_HOST,
                    job='valid_payload_schema', registry=valid_payload_registry)

    return jsonify({
        'status': HTTPStatus.OK.value,
        'payload': request.get_json(),
        'message': 'Valid Schema',
        'error': None
    })


@app.errorhandler(wtforms.validators.ValidationError)
def onValidationError(err):
    invalid_payload_counter.inc()
    push_to_gateway(PUSHGATEWAY_PROMETHEUS_HOST,
                    job='invalid_payload_schema', registry=registry)

    return jsonify({
        'status': HTTPStatus.BAD_REQUEST.value,
        'payload': request.get_json(),
        'message': 'Invalid Schema',
        'error': str(err)
    })


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
