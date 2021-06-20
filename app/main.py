from flask import Flask, request, jsonify, Response
from google.api_core.exceptions import BadRequest
from validator.main import validate_payload
from http import HTTPStatus
import wtforms
import os
app = Flask(__name__)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/chapmon/bootcamps/blank-space-de-batch1/week-4/script/keyfile.json'


@app.route("/", methods=["GET"])
def say_hello():
    return "Hello World, congratulations on installing Flask"


@app.route("/api/activities", methods=["POST"])
def handler():
    print(request.get_json())
    validate_payload(request)

    return jsonify({
        'status': HTTPStatus.OK.value,
        'payload': request.get_json(),
        'message': 'Valid Schema',
        'error': None
    })


@app.errorhandler(wtforms.validators.ValidationError)
def onValidationError(err):
    '''
      TODO: 
        Create CSV/JSON
        Push log ke Grafana dengan tag invalid_schema
    '''

    return jsonify({
        'status': HTTPStatus.BAD_REQUEST.value,
        'payload': request.get_json(),
        'message': 'Invalid Schema',
        'error': str(err)
    })


@app.errorhandler(BadRequest)
def onBadRequestError(err):
    return f'Bad Request! {err}', 400


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
