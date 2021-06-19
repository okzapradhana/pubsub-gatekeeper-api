from flask_inputs.validators import JsonSchema
from flask_inputs import Inputs
from wtforms.validators import ValidationError
from schema import get_schema


class TransactionMessageInputs(Inputs):
    json = [JsonSchema(schema=get_schema())]


def validate_payload(request):
    inputs = TransactionMessageInputs(request)
    if inputs.validate():
        return True
    else:
        raise ValidationError(inputs.errors)
