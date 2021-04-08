from datetime import datetime
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter
from fastapi import Depends
from Services.access_management_service import verify_jwt_token, create_jwt_token
from settings import oauth2_scheme, MICRO_SERVICES_ACCESS_TOKEN, MICRO_SERVICES_ACCESS_TOKEN_EXP_YEARS

router = APIRouter()


@router.post("/generate_token/")
def generate_token(
        token: str = Depends(oauth2_scheme)
):
    payload = verify_jwt_token(token)
    payload["exp"] = (datetime.now() + relativedelta(years=MICRO_SERVICES_ACCESS_TOKEN_EXP_YEARS)).timestamp()
    return create_jwt_token(data=payload, secret_key=MICRO_SERVICES_ACCESS_TOKEN)
