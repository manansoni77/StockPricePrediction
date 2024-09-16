from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379'})

def manual_cache(func):
    def wrapper(*args):
        key = args[0] + func.__name__
        res = cache.get(key)
        if res:
            print('cache hit')
            return res
        res = func(*args)
        print(res)
        if res:
            cache.set(key, res)
        return res
    return wrapper