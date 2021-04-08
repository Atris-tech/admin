# 1. increase user space api
# 2. decrease user space api
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


@router.get("/get_endpoints/")
def get_endpoints(
        token: str = Depends(oauth2_scheme)
):
    verify_jwt_token(token)
    return {
        "nemo": get_val(key="STT_UPLOAD_URL"),
        "f_align": get_val(key="FORCED_ALIGN_UPLOAD_URL"),
        "sound_recog": get_val(key="SOUND_RECOG_ENDPOINT"),
        "enity_recog": get_val(key="ENTITY_ENDPOINT"),
        "summary_key_words_gen": get_val(key="SUMMARY_KEYWORDS_ENDPOINT"),
        "emotion_analysis": get_val(key="EMOTION_ANALYSIS_ENDPOINT")
    }
