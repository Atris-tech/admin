# 1. increase user space api
# 2. decrease user space api
# 5. get stt premium plans
# 6. remove stt premium plans
# 7. change user plan
# 8. get all active users
# 9. get total signup users
# 10. get all premium users
import requests as requests
from fastapi import APIRouter
from fastapi import Depends
from Services.access_management_service import verify_jwt_token
from settings import oauth2_scheme
from Services.redis_service import get_val
from urllib.parse import urlparse

router = APIRouter()


@router.get("/get_endpoints/")
def get_endpoints(
        token: str = Depends(oauth2_scheme)
):
    verify_jwt_token(token)
    endpoints = [
         get_val(key="STT_UPLOAD_URL"),
         get_val(key="FORCED_ALIGN_UPLOAD_URL"),
         get_val(key="SOUND_RECOG_ENDPOINT"),
         get_val(key="ENTITY_ENDPOINT"),
         get_val(key="SUMMARY_KEYWORDS_ENDPOINT"),
         get_val(key="EMOTION_ANALYSIS_ENDPOINT"),
         get_val(key="OCR_ENDPOINT"),
         get_val(key="IMAGE_LABEL_ENPOINT")
    ]
    data = dict()
    data["nemo"] = {"url": endpoints[0]}
    data["f_align"] = {"url": endpoints[1]}
    data["sound_recog"] = {"url": endpoints[2]}
    data["smry_kwrds"] = {"url": endpoints[3]}
    data["entty"] = {"url": endpoints[4]}
    data["emot"] = {"url": endpoints[5]}
    data["ocr"] = {"url": endpoints[6]}
    data["image_label"] = {"url": endpoints[7]}
    for endpoint, data_elem in zip(endpoints, data):
        if endpoint is not None:
            try:
                response = requests.request("GET", str("http://" + urlparse(endpoint).netloc))
                if response.status_code == 200:
                    data[data_elem]["health"] = "Alive"
                elif response.status_code == 404:
                    response = requests.request("GET", str("http://" + urlparse(endpoint).netloc + "/docs"))
                    if response.status_code == 200:
                        data[data_elem]["health"] = "Alive"
                    else:
                        data[data_elem]["health"] = response.status_code
                else:
                    data[data_elem]["health"] = response.status_code
            except requests.exceptions.ConnectionError:
                data[data_elem]["health"] = "Offline"
        else:
            data[data_elem]["health"] = None

    return data
