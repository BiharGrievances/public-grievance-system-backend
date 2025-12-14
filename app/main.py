from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi

from app.database import Base, engine

# Routers
from app.routers import (
    auth_router,
    admin,
    districts,
    panchayats,
    cities,
    complaints,
    attachments
)

# -------------------------------
# DATABASE
# -------------------------------
Base.metadata.create_all(bind=engine)

# -------------------------------
# APP INITIALIZATION
# -------------------------------
app = FastAPI(
    title="Public Grievance & Outreach System",
    description=(
        "A public grievance redressal and outreach platform "
        "for citizen complaints, transparency, and administrative action. "
        "Designed for India with free and open infrastructure."
    ),
    version="1.0.0"
)

# -------------------------------
# SECURITY (OAuth2 for Swagger)
# -------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/auth/login",
                    "scopes": {}
                }
            }
        }
    }

    # Apply globally (admin routes enforce it)
    openapi_schema["security"] = [
        {"OAuth2PasswordBearer": []}
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# -------------------------------
# CORS (Frontend-friendly)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# ROUTERS
# -------------------------------
app.include_router(auth_router.router)      # Auth FIRST
app.include_router(admin.router)             # Admin (JWT protected)
app.include_router(districts.router)
app.include_router(panchayats.router)
app.include_router(cities.router)
app.include_router(complaints.router)        # Public
app.include_router(attachments.router)       # Public uploads

# -------------------------------
# ROOT
# -------------------------------
@app.get("/")
def home():
    return {
        "message": "Public Grievance & Outreach System API is running"
    }
