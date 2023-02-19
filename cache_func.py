from __future__ import annotations

import json

import aioredis

from config.config import Config

redis = aioredis.from_url(f"redis://{Config.REDIS_ADDRESS}")


async def cache_create(name, data):
    await redis.set(name, json.dumps(data))


async def cache_delete_cascade(name):
    key_list = await redis.keys(name)
    if key_list:
        await redis.delete(*key_list)


async def cache_delete(name):
    await redis.delete(name)


async def cache_get(name):
    res = await redis.get(name)
    if res:
        return json.loads(res)
    else:
        return None
    '''key_list = await redis.keys(f"*{name}")
    if key_list:
        name = key_list[0]
        res = await redis.get(name)
        if res:
            return json.loads(await redis.get(name))
        else:
            return None
    return None'''
