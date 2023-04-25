import asyncio
from connection import Connection
from logger import logger


class Tcp(object):

    def __init__(self, port: int, name: str):
        self._port: int = port
        self._name: str = name

    async def run_server(self):
        async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
            connection = Connection(reader, writer)
            remote_connection = await self.connect("xxx", 0000)
            logger.info(f"Client Connected.")
            await asyncio.gather(
                    connection.handle_message(),
                    )

        server = await asyncio.start_server(handle_client, port=self._port)
        logger.info(f"{self._name} Server started on {server.sockets[0].getsockname()}")
        async with server:
            await server.serve_forever()

    @staticmethod
    async def connect(host: str, port: int) -> Connection:
        reader, writer = await asyncio.open_connection(host, port)
        connection = Connection(reader, writer)
        return connection

