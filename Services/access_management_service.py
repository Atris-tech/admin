from db_models.models.user_model import UserModel
from db_models.models.token_model import TokenModel
from Services.redis_service import set_val
from fastapi import HTTPException
import error_constants


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
