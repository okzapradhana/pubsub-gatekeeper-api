from flask import Flask, request, jsonify, Response
from validator import validate_payload
from services import publisher
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
    message = json.dumps(request.get_json()).encode('utf-8')
    print(publisher.push(message))
    return Response('Success', 200)


@app.errorhandler(wtforms.validators.ValidationError)
def onValidationError(err):
    '''
      TODO: 
        Create CSV/JSON
        Push log ke Grafana dengan tag invalid_schema
    '''
    print("Masuk ke onValidationError")
    return Response(f"Validation Error: {str(err)}", 400)


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
