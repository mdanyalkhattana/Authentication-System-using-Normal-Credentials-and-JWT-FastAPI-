from datetime import datetime
from sqlalchemy.ext.declarative import DeclarativeMeta
from fastapi.encoders import jsonable_encoder

class JSONMixin:
    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def to_json(self):
        def convert_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            return obj
        
        return jsonable_encoder(self.to_dict(), custom_encoder={datetime: convert_datetime})