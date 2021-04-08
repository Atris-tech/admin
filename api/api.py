from fastapi import APIRouter

from .endpoints import access_management, acm_login, acm_signup, get_endpoints, set_endpoints, \
    generate_access_token_micro_services

api_router = APIRouter()
api_router.include_router(acm_login.router, tags=["login"])
api_router.include_router(acm_signup.router, tags=["signup"])
api_router.include_router(access_management.router, tags=["access control management"])
api_router.include_router(get_endpoints.router, tags=['get_endpoints'])
api_router.include_router(set_endpoints.router, tags=['set_endpoints'])
api_router.include_router(generate_access_token_micro_services.router, tags=['generate_access_token_micro_services'])
