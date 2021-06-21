from flask import Flask, request, jsonify, Response
from google.api_core.exceptions import BadRequest
from prometheus_client.utils import INF
from validator.main import validate_payload
from http import HTTPStatus
from dotenv import load_dotenv
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
import wtforms
import os
import time

load_dotenv()
os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

app = Flask(__name__)
graphs = {}
graphs['c'] = Counter('python_request_operations_total',
                      'The total number of processed requests')
graphs['h'] = Histogram('python_request_duration_seconds',
                        'Histogram for the duration in seconds', buckets=(1, 2, 3, 5, 8, 13, 21, INF))


@app.route("/")
def say_hello():
    start = time.time()
    graphs['c'].inc()

    # time.sleep(2)
    end = time.time()
    graphs['h'].observe(end - start)
    return "Hello World, congratulations on installing Flask"


@app.route("/metrics")
def count_requests():
    res = []
    for _, val in graphs.items():
        res.append(prometheus_client.generate_latest(val))
    return Response(res, mimetype="text/plain")


@app.route("/api/activities", methods=["POST"])
def handler():
    validate_payload(request)

    return jsonify({
        'status': HTTPStatus.OK.value,
        'payload': request.get_json(),
        'message': 'Valid Schema',
        'error': None
    })


@app.errorhandler(wtforms.validators.ValidationError)
def onValidationError(err):

    return jsonify({
        'status': HTTPStatus.BAD_REQUEST.value,
        'payload': request.get_json(),
        'message': 'Invalid Schema',
        'error': str(err)
    })


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
