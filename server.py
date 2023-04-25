import asyncio
from connection import Connection
from logger import logger
from typing import Tuple


class TcpServer(object):

    def __init__(self, port: int,):
        self._port: int = port

    async def run_server(self):
        async def handle_client(local_reader: asyncio.StreamReader, local_writer: asyncio.StreamWriter):
            remote_reader, remote_writer = await self.connect("xxx", 0000)
            connection_local = Connection(local_reader, remote_writer)
            connection_remote = Connection(remote_reader, local_writer)
            await asyncio.gather(
                    connection_local.handle_message(),
                    connection_remote.handle_message(),
                    )

        server = await asyncio.start_server(handle_client, port=self._port)
        logger.info(f"ShadowSocks Server started on {server.sockets[0].getsockname()}")
        async with server:
            await server.serve_forever()

    @staticmethod
    async def connect(host: str, port: int) -> Tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        reader, writer = await asyncio.open_connection(host, port)
        return reader, writer

if __name__ == '__main__':
    logger.init_logger()

    s = TcpServer(8888)
    loop = asyncio.get_event_loop()
    loop.create_task(s.run_server())
    loop.run_forever()


