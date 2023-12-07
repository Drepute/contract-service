import traceback

from flask import current_app as app



class RedisError(Exception): ...

import structlog
logger = structlog.get_logger()

def get_redis_connection():
    if not app.config['USE_CACHE']:
        return None
    # connection = redis.StrictRedis(host=app.config['REDIS_URL']['HOST'],
    #                                port=app.config['REDIS_URL']['PORT'],
    #                                db=app.config['REDIS_URL']['DB'])
    connection = app.redis_connection
    return connection


def get_from_redis(key):
    try:
        redis_conn = get_redis_connection()
        if redis_conn:
            value = redis_conn.get(key)
            try:
                value = value.decode('utf-8')
            except:
                pass
            return value
    except RedisError as e:
        logger.error("get_redis_connection : Could not get connection")
        logger.error("Redis Error in get_redis_connection")
        traceback.print_exc()
        app.apm.capture_exception()
    except Exception as e:
        logger.error("get_redis_connection : Could not get connection")
        logger.error("Unknown Error in get_redis_connection")
        traceback.print_exc()
        app.apm.capture_exception()
    return None


def get_multi_from_redis(keys):
    key_value_dict = {}
    try:
        redis_conn = get_redis_connection()
        if redis_conn:
            values = redis_conn.mget(keys)
            try:
                for i in range(0, len(keys)):
                    if values[i] is not None:
                        value = values[i].decode('utf-8')
                        key_value_dict[keys[i]] = value
            except:
                pass
            return key_value_dict
    except RedisError as e:
        logger.error("get_redis_connection : Could not get connection")
        logger.error("Redis Error in get_redis_connection")
        traceback.print_exc()
        app.apm.capture_exception()
    except Exception as e:
        logger.error("get_redis_connection : Could not get connection")
        logger.error("Unknown Error in get_redis_connection")
        traceback.print_exc()
        app.apm.capture_exception()
    return None


def set_in_redis(key, value, expiry=None):
    try:
        redis_conn = get_redis_connection()
        if redis_conn:
            if expiry is None:
                expiry = 60 * 60 * 24 * 30  # in seconds 30 days
            redis_conn.setex(key, expiry, value)
            return value
    except RedisError as e:
        logger.error("get_redis_connection : Could not get connection")
        logger.error("Redis Error in get_redis_connection")
        traceback.print_exc()
        app.apm.capture_exception()
    except Exception as e:
        logger.error("get_redis_connection : Could not get connection")
        logger.error("Unknown Error in get_redis_connection")
        traceback.print_exc()
        app.apm.capture_exception()
    return None


def delete_from_redis(key):
    try:
        redis_conn = get_redis_connection()
        if redis_conn:
            redis_conn.delete(key)
    except RedisError as e:
        logger.error("get_redis_connection : Could not get connection")
        logger.error("Redis Error in get_redis_connection")
        traceback.print_exc()
        app.apm.capture_exception()
    except Exception as e:
        logger.error("get_redis_connection : Could not get connection")
        logger.error("Unknown Error in get_redis_connection")
        traceback.print_exc()
        app.apm.capture_exception()
    return None


def delete_keys_from_redis_matching_pattern(pattern):
    try:
        redis_conn = get_redis_connection()
        if redis_conn:
            for k in redis_conn.scan_iter(pattern):
                redis_conn.delete(k)
    except RedisError as e:
        logger.error("get_redis_connection : Could not get connection")
        logger.error("Redis Error in get_redis_connection")
        traceback.print_exc()
        app.apm.capture_exception()
    except Exception as e:
        logger.error("get_redis_connection : Could not get connection")
        logger.error("Unknown Error in get_redis_connection")
        traceback.print_exc()
        app.apm.capture_exception()
    return None


def incr_key(key):
    try:
        redis_conn = get_redis_connection()
        if redis_conn:
            redis_conn.incr(key)
    except RedisError as e:
        logger.error("get_redis_connection : Could not get connection")
        logger.error("Redis Error in get_redis_connection")
        traceback.print_exc()
        app.apm.capture_exception()
    except Exception as e:
        logger.error("get_redis_connection : Could not get connection")
        logger.error("Unknown Error in get_redis_connection")
        traceback.print_exc()
        app.apm.capture_exception()
    return None


def decr_key(key):
    try:
        redis_conn = get_redis_connection()
        if redis_conn:
            redis_conn.decr(key)
    except RedisError as e:
        logger.error("get_redis_connection : Could not get connection")
        logger.error("Redis Error in get_redis_connection")
        traceback.print_exc()
        app.apm.capture_exception()
    except Exception as e:
        logger.error("get_redis_connection : Could not get connection")
        logger.error("Unknown Error in get_redis_connection")
        traceback.print_exc()
        app.apm.capture_exception()
    return None
