from db_models.models.user_model import UserModel
from db_models.models.token_model import TokenModel
from Services.redis_service import set_val
from fastapi import HTTPException
import error_constants
from jose import JWTError, jwt
import settings


def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError as e:
        """LOG JWT ERROR HERE"""
        print(e)
        return HTTPException(
            status_code=error_constants.TOKEN_EXPIRED_INVALID["status_code"],
            detail=error_constants.TOKEN_EXPIRED_INVALID["detail"]
        )


def create_jwt_token(data, secret_key=False):
    print(data)
    to_encode = data.copy()
    if secret_key:
        secret_key_jwt = secret_key
    else:
        secret_key_jwt = settings.JWT_SECRET_KEY
    encoded_jwt = jwt.encode(to_encode, secret_key_jwt, algorithm=settings.JWT_ALGORITHM)
    print(encoded_jwt)
    return encoded_jwt


def check_user(email):
    try:
        user_obj = UserModel.objects.get(email_id=email)
        return user_obj
    except UserModel.DoesNotExist:
        return HTTPException(
            status_code=error_constants.INVALID_EMAIL["status_code"],
            detail=error_constants.INVALID_EMAIL["detail"]
        )


def check_token(user_obj, ban):
    try:
        token_obj = TokenModel.objects.get(user=user_obj)
        if ban:
            token_obj.token_status = "Dead"
        else:
            token_obj.token_status = "Alive"
        token_obj.save()
        ref_token = token_obj.refresh_token
        if ban:
            if ref_token is not None:
                set_val(ref_token, {"banned": True}, json_type=True)
        else:
            if ref_token is not None:
                set_val(ref_token, None, json_type=True)
    except TokenModel.DoesNotExist:
        if ban:
            token_status = "Dead"
        else:
            token_status = "Alive"
        token_obj = TokenModel(
            user=user_obj,
            refresh_token=None,
            token_status=token_status
        )
        token_obj.save()


def ban_user(email):
    check_token(user_obj=check_user(email), ban=True)


def unban_user(email):
    check_token(user_obj=check_user(email), ban=False)
