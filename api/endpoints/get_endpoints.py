# 1. increase user space api
# 2. decrease user space api
# 5. get stt premium plans
# 6. remove stt premium plans
# 8. get all active users
# 9. get total signup users
# 10. get all premium users
import requests
from fastapi import APIRouter
from fastapi import Depends
from Services.access_management_service import verify_jwt_token
from settings import oauth2_scheme
from Services.redis_service import get_val
from urllib.parse import urlparse
import asyncio

router = APIRouter()


async def health_api_call(endpoint):
    try:
        response = requests.get(str("http://" + urlparse(endpoint).netloc), timeout=4)
        if response.status_code == 200:
            return "Alive"
        elif response.status_code == 404:
            response = requests.get(str("http://" + urlparse(endpoint).netloc + "/docs"), timeout=4)
            if response.status_code == 200:
                return "Alive"
            else:
                return response.status_code
        else:
            return response.status_code
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return "Offline"


@router.get("/get_endpoints_health/")
async def get_endpoints_health(
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
    tasks = list()
    for endpoint, data_elem in zip(endpoints, data):
        if endpoint is not None:
            tasks.append(health_api_call(endpoint))
    results = await asyncio.gather(*tasks)
    for endpoint, data_elem, health in zip(endpoints, data, results):
        if endpoint is not None:
            data[data_elem]["health"] = health
        else:
            data[data_elem]["health"] = None
    return data


@router.get("/get_endpoints")
def get_endpoints(
        token: str = Depends(oauth2_scheme)
):
    verify_jwt_token(token)
    data = dict()
    data["nemo"] = get_val(key="STT_UPLOAD_URL")
    data["f_align"] = get_val(key="FORCED_ALIGN_UPLOAD_URL")
    data["sound_recog"] = get_val(key="SOUND_RECOG_ENDPOINT")
    data["smry_kwrds"] = get_val(key="SUMMARY_KEYWORDS_ENDPOINT")
    data["entty"] = get_val(key="ENTITY_ENDPOINT")
    data["emot"] = get_val(key="EMOTION_ANALYSIS_ENDPOINT")
    data["ocr"] = get_val(key="OCR_ENDPOINT")
    data["image_label"] = get_val(key="IMAGE_LABEL_ENPOINT")
    return data
