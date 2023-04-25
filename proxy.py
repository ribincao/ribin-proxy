from logger import logger
from typing import Tuple
import asyncio


async def handle_message(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            writer.write(data)
            # await writer.drain()
    except Exception as error:
        logger.error(f"handle_tcp error {error}")


class Proxy(object):

    def __init__(self, port: int,):
        self._port: int = port

    async def run_server(self):
        async def call_back(local_reader: asyncio.StreamReader, local_writer: asyncio.StreamWriter):
            # TODO: 发起连接
            remote_reader, remote_writer = await self.connect("xxx", 0000)

            await asyncio.gather(
                    handle_message(local_reader, remote_writer),
                    handle_message(remote_reader, local_writer)
                    )

        server = await asyncio.start_server(call_back, port=self._port)
        logger.info(f"ShadowSocks Server started on {server.sockets[0].getsockname()}")
        async with server:
            await server.serve_forever()


    async def run_client(self):
        remote_reader, remote_writer = await self.connect("xxxx", 8888)  # 连接server

        async def call_back(local_reader: asyncio.StreamReader, local_writer: asyncio.StreamWriter):
            await asyncio.gather(
                    handle_message(local_reader, remote_writer),
                    handle_message(remote_reader, local_writer)
                    )

        server = await asyncio.start_server(call_back, port=self._port)
        logger.info(f"ShadowSocks Client Started on {server.sockets[0].getsockname()}")
        async with server:
            await server.serve_forever()

    @staticmethod
    async def connect(host: str, port: int) -> Tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        reader, writer = await asyncio.open_connection(host, port)
        return reader, writer

if __name__ == '__main__':
    logger.init_logger()

    proxy = Proxy(8888)
    loop = asyncio.get_event_loop()
    # loop.create_task(proxy.run_client())
    loop.create_task(proxy.run_server())
    loop.run_forever()


