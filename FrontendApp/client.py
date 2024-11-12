import json
import aiohttp
import asyncio


url = "http://localhost:8001/stream"


async def get_event():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            while True:
                data_chunk = await response.content.readline()
                print(data_chunk, type(data_chunk))
                if not data_chunk:
                    break
                yield json.loads(data_chunk.decode("utf-8"))


async def main():
    async for event in get_event():
        print(event)


asyncio.run(main())
