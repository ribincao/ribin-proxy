from logger import logger
from typing import Tuple
import asyncio




class Test(object):

    def __init__(self, port: int,):
        self._port: int = port

    async def run(self):
        reader, writer = await self.connect("localhost", self._port)  # 连接server

        async def test_message(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
            while True:
                data = b"hello"
                writer.write(data)
                await asyncio.sleep(1)

        await test_message(reader, writer)


    @staticmethod
    async def connect(host: str, port: int) -> Tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        reader, writer = await asyncio.open_connection(host, port)
        return reader, writer

if __name__ == '__main__':
    logger.init_logger()

    test = Test(8088)
    loop = asyncio.get_event_loop()
    loop.create_task(test.run())
    loop.run_forever()


