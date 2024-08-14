from redis.asyncio import Redis as AsyncioRedis


REDIS_HOST = 'localhost'
REDIS_PORT = 6379


class AsyncCacheSystemPlugin:
    def __init__(self, host: str = REDIS_HOST, port: int = REDIS_PORT, db_section: int = 0):
        self._redis = AsyncioRedis(host=host,
                                   port=port,
                                   db=db_section,
                                   decode_responses=True)

    @property
    def redis(self):
        return self._redis

    async def send_data(self, data_packets: list[dict]):
        for packet in data_packets:
            await self.redis.set(packet.get('url'), str(packet))

    async def get_actual_content(self):
        redis_section = self._redis[0]
        all_content_blocks = [key for key in redis_section.scan_iter()]
        print(all_content_blocks)
        result = []
        for block_key in all_content_blocks:
            result.append(redis_section.get(block_key))
        return result
