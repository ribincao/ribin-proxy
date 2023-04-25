
import asyncio
from logger import logger


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
