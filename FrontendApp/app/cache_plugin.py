import json
import logging
import os

import redis
from redis.asyncio import Redis as AsyncioRedis
from redis import Redis

from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

CACHE_HOST = os.getenv('CACHE_HOST')
CACHE_PORT = os.getenv('CACHE_PORT')


class AsyncCacheSystemPlugin:
    def __init__(self, host: str = CACHE_HOST, port: int = CACHE_PORT, db_section: int = 0):
        self._async_redis = AsyncioRedis(host=host,
                                         port=port,
                                         db=db_section,
                                         decode_responses=True)
        self._sync_redis = Redis(host=host,
                                 port=port,
                                 db=db_section,
                                 decode_responses=True)

    def check(self):
        self._sync_redis.ping()

    def set_mapping(self, data: dict):
        with self._sync_redis.pipeline() as pipe:
            for key, item in data.items():
                if isinstance(item, dict):
                    pipe.hset(key, mapping=item)
                else:
                    pipe.set(key, str(item))
            pipe.execute()
        self._sync_redis.bgsave()

    def set_expired_key(self, key, value, minutes=1):
        """Set key with timeout. After some time key and value will be deleted."""
        self._sync_redis.setex(key, timedelta(minutes=minutes), value=value)

    def make_snapshot(self):
        last_save_datetime = self._sync_redis.lastsave()

        self._sync_redis.bgsave()

    def _prepare_storage_with_data(self, data):
        pass

    def pipe_watch_example(self, item_id: int, first_field: str, second_field: str):
        logging.basicConfig()

        class SomeError(Exception):
            """Some error"""

        with self._sync_redis.pipeline() as pipe:
            error_count = 0
            while True:
                try:
                    pipe.watch(str(item_id))
                    n_left = self._sync_redis.hget(str(item_id), first_field)
                    if n_left:
                        pipe.multi()
                        pipe.hincrby(str(item_id), first_field, -1)
                        pipe.hincrby(str(item_id), second_field, 1)
                        pipe.execute()
                        break
                    else:
                        pipe.unwatch()
                        logging.error("error")
                        raise SomeError("Some error!")
                except redis.WatchError:
                    error_count += 1
                    logging.warning("WatchError #%d: %s; retrying", error_count, item_id)

    def load_initial_data(self, initial_dump_path: str) -> None:
        redis_client = self._sync_redis
        if os.path.exists(initial_dump_path) and initial_dump_path.endswith('.json'):
            with open(initial_dump_path) as f:
                data = json.load(f)
            for block_key, block_structure in data.items():
                redis_client.set(block_key, json.dumps(block_structure))
        else:
            raise Exception(f"Json file in path {initial_dump_path} doesn't exist")

    async def send_data(self, data_packets: list[dict]):
        for packet in data_packets:
            # await self._async_redis.set(packet.get('url'), str(packet))
            if packet.get('url'):
                await self._async_redis.json().set(packet.get('url'), "$", packet)

    async def get_actual_content(self):
        redis_section = self._sync_redis
        all_content_blocks = [key for key in redis_section.scan_iter()]
        result = []
        print('keys =', all_content_blocks)
        for block_key in all_content_blocks:
            result.append(redis_section.json().get(block_key, f"$.{block_key}"))
        return result


if __name__ == '__main__':
    client = AsyncCacheSystemPlugin()
    client.set_mapping({'qwe': '123'})
    client.set_expired_key('test1235', 12345, 1)
