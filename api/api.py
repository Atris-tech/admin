from fastapi import APIRouter

from .endpoints import access_management, acm_login, acm_signup

api_router = APIRouter()
api_router.include_router(acm_login.router, tags=["login"])
api_router.include_router(acm_signup.router, tags=["signup"])
api_router.include_router(access_management.router, tags=["access control management"])