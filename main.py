from fastapi import FastAPI
from routes import auth_routes, verify_routes
from database import Base, engine
from routes import session_routes
from routes import password_routes


# from routes import auth_routes, verify_routes


app = FastAPI(title="Authentication System")

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)
app.include_router(verify_routes.router)
app.include_router(session_routes.router)
app.include_router(password_routes.router)
# app.include_router(auth_routes.router)
# app.include_router(auth_routes.router)

