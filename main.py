from fastapi import FastAPI
from fastapi.responses import JSONResponse
from database import Base, engine
from routes import auth_routes, password_routes, verification_routes
from datetime import datetime
from fastapi.encoders import jsonable_encoder
import json

# Create all database tables (only runs if they don't exist)
Base.metadata.create_all(bind=engine)

class CustomJSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        if content is None:
            return b""
        
        def convert_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            return obj

        json_content = jsonable_encoder(content, custom_encoder={datetime: convert_datetime})
        return json.dumps(
            json_content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")

# Initialize FastAPI app
app = FastAPI(
    title="Authentication System",
    description="A complete authentication system using FastAPI and MySQL",
    version="1.0.0",
    default_response_class=CustomJSONResponse
)

# Include all route files
app.include_router(auth_routes.router)
app.include_router(password_routes.router)
app.include_router(verification_routes.router)


