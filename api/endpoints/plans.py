from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel

from Services.access_management_service import verify_jwt_token
from settings import oauth2_scheme
from Services.redis_service import get_list, add_to_list


router = APIRouter()


@router.get("/get_paid_plan_details/")
def get_endpoints(
        token: str = Depends(oauth2_scheme)
):
    verify_jwt_token(token)
    return {
        "plan_info": get_list("DIRECT_STT_API_PLANS")
    }


class PlanDetails(BaseModel):
    plan_names: list


@router.post("/update_paid_plans/")
def set_plan_info(
        plan_details_obj: PlanDetails,
        token: str = Depends(oauth2_scheme)
):
    verify_jwt_token(token)
    add_to_list("DIRECT_STT_API_PLANS", plan_details_obj.plan_names)
    return True