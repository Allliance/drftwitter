from redis import Redis

REDIS_DATABASE = None


def initialize():
    global REDIS_DATABASE
    REDIS_DATABASE = Redis()


def get_user_data(id):
    global REDIS_DATABASE
    if REDIS_DATABASE is None:
        initialize()
        return None
    return REDIS_DATABASE.get(id).decode('utf-8') if REDIS_DATABASE.get(id) is not None else None


def cache_data(id, data, exp_time=300):
    global REDIS_DATABASE
    if REDIS_DATABASE is None:
        initialize()
        return None
    REDIS_DATABASE.setex(id, exp_time, data)


