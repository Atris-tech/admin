# 1. increase user space api
# 2. decrease user space api
# 3. get stt_endpoint
# 4. change stt_endpoint
# 5. get stt premium plans
# 6. remove stt premium plans
# 7. change user plan
# 8. get all active users
# 9. get total signup users
# 10. get all premium users

from fastapi import APIRouter
from fastapi import Depends
from Services.access_management_service import verify_jwt_token
from settings import oauth2_scheme
from Services.redis_service import get_val

router = APIRouter()


@router.get("/stt_endpoints/")
def ban(
        token: str = Depends(oauth2_scheme)
):
    verify_jwt_token(token)
    stt_end_point = get_val(key="STT_UPLOAD_URL")
    f_align_end_point = get_val(key="FORCED_ALIGN_UPLOAD_URL")
    sound_recog_endpoint = get_val(key="SOUND_RECOG_ENDPOINT")
    return {
        "nemo": stt_end_point,
        "f_align": f_align_end_point,
        "sound_recog": sound_recog_endpoint
    }