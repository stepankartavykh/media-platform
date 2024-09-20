import asyncio
import json
import os

from redis.asyncio import Redis as AsyncioRedis
from redis import Redis

REDIS_HOST = 'localhost'
REDIS_PORT = 6379


class AsyncCacheSystemPlugin:
    def __init__(self, host: str = REDIS_HOST, port: int = REDIS_PORT, db_section: int = 0):
        self._async_redis = AsyncioRedis(host=host,
                                         port=port,
                                         db=db_section,
                                         decode_responses=True)
        self._sync_redis = Redis(host=host,
                                 port=port,
                                 db=db_section,
                                 decode_responses=True)

    def load_initial_data(self, initial_dump_path: str) -> None:
        redis_client = self._sync_redis
        if os.path.exists(initial_dump_path) and initial_dump_path.endswith('.json'):
            with open(initial_dump_path) as f:
                data = json.load(f)
            if not data.get('itemsBlocks'):
                raise Exception('Interface in data is incorrect!')
            for block_key, block_structure in data['itemsBlocks'].items():
                redis_client.json().set(block_structure.get('url', block_key), "$", block_structure)
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
    # client.load_initial_data()
    print('result =', asyncio.run(client.get_actual_content()))
