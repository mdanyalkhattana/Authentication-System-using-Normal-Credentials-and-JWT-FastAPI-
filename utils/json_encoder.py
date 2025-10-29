from datetime import datetime
from json import JSONEncoder
from fastapi.encoders import jsonable_encoder

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return jsonable_encoder(obj)