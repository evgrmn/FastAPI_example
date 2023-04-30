from __future__ import annotations

import json

import aioredis

from config.config import Env

redis = aioredis.from_url(f"redis://{Env.REDIS_ADDRESS}")


async def set(name, data):
    await redis.set(name, json.dumps(data))


async def delete_cascade(name):
    key_list = await redis.keys(name)
    if key_list:
        await redis.delete(*key_list)


async def delete(name):
    await redis.delete(name)


async def get(name):
    res = await redis.get(name)
    if res:
        return json.loads(res)
    else:
        return None


async def keys(find):
    key_list = await redis.keys(f"{find}*")

    return key_list
