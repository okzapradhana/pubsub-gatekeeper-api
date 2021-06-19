from flask_inputs.validators import JsonSchema
from flask_inputs import Inputs
from google.api_core.exceptions import BadRequest
from wtforms.validators import ValidationError
from validator.schema import get_schema
from services import publisher
import json


class TransactionMessageInputs(Inputs):
    json = [JsonSchema(schema=get_schema())]


def validate_payload(request):
    inputs = TransactionMessageInputs(request)
    try:
        if inputs.validate():
            message = json.dumps(request.get_json()).encode('utf-8')
            publisher.push(message)
    except ValidationError:
        raise ValidationError(inputs.errors)
