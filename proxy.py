from logger import logger
from typing import Tuple
import asyncio


class Connection(object):

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, is_remote=False):
        self._reader: asyncio.StreamReader = reader
        self._writer: asyncio.StreamWriter = writer
        self.is_close: bool = False
        self.is_remote: bool = is_remote

    def close(self):
        self._writer.close()
        self.is_close = True

    async def read(self, n: int) -> bytes:
        data = await self._reader.read(n)
        return data


    async def write(self, data: bytes):
        self._writer.write(data)
        # await self._writer.drain()


async def transport(conn_1: Connection, conn_2: Connection):
    try:
        while not conn_1.is_close:
            data = await conn_1.read(1024)
            if not data:
                break
            logger.info(f"transport data: {data}")
            await conn_2.write(data)
        conn_1.close()

    except Exception as error:
        logger.error(f"tranport error {error}")


class Proxy(object):

    def __init__(self, port: int):
        self._port: int = port

    async def run_server(self):
        async def call_back(local_reader: asyncio.StreamReader, local_writer: asyncio.StreamWriter):
            # TODO: 首包拆包, 发起连接
            logger.info(f"[Server] Connected.")
            remote_reader, remote_writer = await self.connect("xxx", 0000)

            remote_conn = Connection(remote_reader, remote_writer)
            local_conn = Connection(local_reader, local_writer)

            await asyncio.gather(
                    transport(local_conn, remote_conn),
                    transport(remote_conn, local_conn)
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

            remote_conn = Connection(remote_reader, remote_writer)
            local_conn = Connection(local_reader, local_writer)
            await asyncio.gather(
                    transport(local_conn, remote_conn),
                    transport(remote_conn, local_conn)
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


