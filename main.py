from flask import Flask, request, jsonify, Response
from google.api_core.exceptions import BadRequest
from validator.main import validate_payload
import wtforms
import json
import os
app = Flask(__name__)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/chapmon/bootcamps/blank-space-de-batch1/week-4/script/keyfile.json'


@app.route("/", methods=["GET"])
def say_hello():
    return "Hello World, congratulations on installing Flask"


@app.route("/api/activities", methods=["POST"])
def processor():
    print(request.get_json())
    is_valid = validate_payload(request)
    return jsonify({
        'status': 200,
        'is_schema_valid': is_valid,
        'message': 'Schema is valid and the data has been pushed to PubSub Topic'
    })


@app.errorhandler(wtforms.validators.ValidationError)
def onValidationError(err):
    '''
      TODO: 
        Create CSV/JSON
        Push log ke Grafana dengan tag invalid_schema
    '''
    print("Masuk ke onValidationError")
    return Response(f"Validation Error: {str(err)}", 400)


@app.errorhandler(BadRequest)
def onBadRequestError(err):
    return f'Bad Request! {err}', 400


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
