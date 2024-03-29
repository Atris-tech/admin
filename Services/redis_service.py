import redis
import settings
import json

redis_obj = redis.StrictRedis(host=settings.REDIS_HOSTNAME, port=settings.REDIS_PORT,
                              password=settings.REDIS_PASSWORD, ssl=True, decode_responses=True)


def set_val(key, val, json_type=False):
    if json_type:
        redis_obj.set(key, json.dumps(val))
    else:
        redis_obj.set(key, str(val))


def get_val(key, json_type=False):
    if json_type:
        try:
            u_data = redis_obj.get(key)
            if u_data is not None:
                data = json.loads(u_data)
                return data
            else:
                return None
        except ValueError:
            return False
    else:
        return redis_obj.get(key)


def get_list(list_name):
    results = list()
    for i in range(0, redis_obj.llen(list_name)):
        results.append(redis_obj.lindex(list_name, i))
    return results


def add_to_list(list_name, val):
    if type(val) == list:
        for element in val:
            redis_obj.lpush(list_name, element)
    elif type(val) == str:
        redis_obj.lpush(list_name, val)