import asyncio
from logger import logger
from typing import Tuple


class Connection(object):

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        super(Connection, self).__init__()
        self._reader: asyncio.StreamReader = reader
        self._writer: asyncio.StreamWriter = writer
        self._is_close: bool = False

    def close(self):
        if self._is_close:
            return
        self._writer.close()
        self._is_close = True

    async def handle_tcp(self):
        try:
            while not self._is_close:
                data = await self._reader.read(1024)
                if not data:
                    break
                self._writer.write(data)
                # await self.writer.drain()
        except Exception as error:
            logger.error(f"handle_tcp error {error}")
            self.close()


class TcpServer(object):

    def __init__(self, port: int,):
        self._port: int = port

    async def run_server(self):
        async def handle_client(local_reader: asyncio.StreamReader, local_writer: asyncio.StreamWriter):
            # TODO: 发起连接
            remote_reader, remote_writer = await self.connect("xxx", 0000)

            connection_local = Connection(local_reader, remote_writer)
            connection_remote = Connection(remote_reader, local_writer)
            await asyncio.gather(
                    connection_local.handle_tcp(),
                    connection_remote.handle_tcp(),
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


