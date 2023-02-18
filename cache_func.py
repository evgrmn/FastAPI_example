from __future__ import annotations

import json

import aioredis

from config.config import Config


class Connect:
    redis = aioredis.from_url(f"redis://{Config.REDIS_ADDRESS}")


connect = Connect()


async def cache_create(name, data):
    # redis = aioredis.from_url(f"redis://{Config.REDIS_ADDRESS}")
    await connect.redis.set(name, json.dumps(data))


async def cache_delete_cascade(name):
    # redis = aioredis.from_url(f"redis://{Config.REDIS_ADDRESS}")
    key_list = await connect.redis.keys(name)
    if key_list:
        await connect.redis.delete(*key_list)


async def cache_delete(name):
    # redis = aioredis.from_url(f"redis://{Config.REDIS_ADDRESS}")
    await connect.redis.delete(name)


async def cache_update(name, data):
    # redis = aioredis.from_url(f"redis://{Config.REDIS_ADDRESS}")
    key_list = await connect.redis.keys(f"*{name}")
    if key_list:
        name = key_list[0]
        res = json.loads(await connect.redis.get(name))
        res.update(data)
        await cache_create(name, res)


async def cache_get(name):
    # redis = aioredis.from_url(f"redis://{Config.REDIS_ADDRESS}")
    key_list = await connect.redis.keys(f"*{name}")
    if key_list:
        name = key_list[0]
        res = await connect.redis.get(name)
        if res:
            return json.loads(await connect.redis.get(name))
        else:
            return None
    return None
