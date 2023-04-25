from logger import logger
from typing import Tuple
import asyncio


async def transport(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        while True:
            data = await reader.read(1024)
            logger.info(f"transport data: {data}")
            if not data:
                break
            writer.write(data)
            # await writer.drain()
    except Exception as error:
        logger.error(f"handle_tcp error {error}")


class Proxy(object):

    def __init__(self, port: int,):
        self._port: int = port

    async def test_server(self):
        async def test_call_back(local_reader: asyncio.StreamReader, local_writer: asyncio.StreamWriter):
            logger.info(f"[TestServer] Connected.")
            while True:
                data = await local_reader.read(1024)
                if not data:
                    break
                logger.info(f"Test Server Receive {data}")
        server = await asyncio.start_server(test_call_back, port=self._port)
        logger.info(f"Test ShadowSocks Server started on {server.sockets[0].getsockname()}")
        async with server:
            await server.serve_forever()

    async def run_server(self):
        async def call_back(local_reader: asyncio.StreamReader, local_writer: asyncio.StreamWriter):
            # TODO: 首包拆包, 发起连接
            remote_reader, remote_writer = await self.connect("xxx", 0000)

            await asyncio.gather(
                    transport(local_reader, remote_writer),
                    transport(remote_reader, local_writer)
                    )

        server = await asyncio.start_server(call_back, port=self._port)
        logger.info(f"ShadowSocks Server started on {server.sockets[0].getsockname()}")
        async with server:
            await server.serve_forever()


    async def run_client(self):
        remote_reader, remote_writer = await self.connect("localhost", 8888)  # 连接server
        # TODO: 封装首包

        async def call_back(local_reader: asyncio.StreamReader, local_writer: asyncio.StreamWriter):
            logger.info(f"[Client] Connected.")
            await asyncio.gather(
                    transport(local_reader, remote_writer),
                    transport(remote_reader, local_writer)
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


