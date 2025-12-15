from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi

from app.database import Base, engine

# 🔴 IMPORTANT: import ALL models BEFORE create_all
from app.models.admin_user import AdminUser
from app.models.complaint import Complaint
from app.models.district import District
from app.models.panchayat import Panchayat
from app.models.city import City
from app.models.attachment import Attachment

# Create tables
Base.metadata.create_all(bind=engine)

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

app = FastAPI(
    title="Public Grievance & Outreach System",
    description=(
        "An initiative by Dr. Ashutosh Singh — "
        "a public grievance redressal and outreach platform "
        "for citizen complaints, transparency, and administrative action in India."
    ),
    version="1.0.0"
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    schema["components"]["securitySchemes"] = {
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

    schema["security"] = [{"OAuth2PasswordBearer": []}]
    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(admin.router)
app.include_router(districts.router)
app.include_router(panchayats.router)
app.include_router(cities.router)
app.include_router(complaints.router)
app.include_router(attachments.router)

@app.get("/")
def home():
    return {
        "initiative": "AN INITIATIVE BY Dr. ASHUTOSH SINGH",
        "description": (
            "Public Grievance & Outreach System — a citizen-focused platform "
            "for grievance redressal, transparency, and administrative action in Bihar and India."
        ),
        "status": "API is running"
    }
