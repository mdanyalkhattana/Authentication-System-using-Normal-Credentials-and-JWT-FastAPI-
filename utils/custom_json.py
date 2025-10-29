# from fastapi.responses import JSONResponse
# from datetime import datetime
# import json

# class CustomJSONResponse(JSONResponse):
#     def render(self, content) -> bytes:
#         def datetime_handler(obj):
#             if isinstance(obj, datetime):
#                 return obj.isoformat()
#             raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

#         return json.dumps(
#             content,
#             default=datetime_handler,
#             ensure_ascii=False,
#             allow_nan=False,
#             indent=None,
#             separators=(",", ":")
#         ).encode("utf-8")