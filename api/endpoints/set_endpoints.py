from fastapi import APIRouter
from fastapi import Depends
from Services.access_management_service import verify_jwt_token
from settings import oauth2_scheme
from pydantic import HttpUrl, BaseModel
from Services.redis_service import set_val

router = APIRouter()


class EndpointsModel(BaseModel):
    nemo: HttpUrl
    f_align: HttpUrl
    sound_recog: HttpUrl
    smry_kwrds: HttpUrl
    entty: HttpUrl
    emot: HttpUrl


@router.post("/set_endpoints/")
def set_endpoints(
        endpoint_obj: EndpointsModel,
        token: str = Depends(oauth2_scheme),
):
    verify_jwt_token(token)
    set_val(key="STT_UPLOAD_URL", val=endpoint_obj.nemo)
    set_val(key="FORCED_ALIGN_UPLOAD_URL", val=endpoint_obj.f_align)
    set_val(key="SOUND_RECOG_ENDPOINT", val=endpoint_obj.sound_recog)
    set_val(key="SUMMARY_KEYWORDS_ENDPOINT",  val=endpoint_obj.smry_kwrds)
    set_val(key="ENTITY_ENDPOINT", val=endpoint_obj.entty)
    set_val(key="EMOTION_ANALYSIS_ENDPOINT", val=endpoint_obj.emot)
    return True
