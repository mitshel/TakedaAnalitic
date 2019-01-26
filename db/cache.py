from django.core.cache import cache
from django.conf import settings


def clear_cache(org_id):
    if settings.CACHES['default']['BACKEND'] == 'django_redis.cache.RedisCache':
        n = cache.delete_pattern("*", version=org_id)
    else:
        cache.clear()
        n = -1

    return n