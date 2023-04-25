
import asyncio
from typing import Optional
from logger import logger
from buffer import Buffer
from codec import Codec
import time


class Connection(object):

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        super(Connection, self).__init__()
        self.reader: asyncio.StreamReader = reader
        self.writer: asyncio.StreamWriter = writer
        self.buffer: Buffer = Buffer()
        self.codec: Codec = Codec()
        self._is_close: bool = False
        self.last_active_time: int = int(time.time())

    def update_active_time(self):
        self.last_active_time = int(time.time())

    def close(self):
        if self._is_close:
            return
        self.writer.close()
        self._is_close = True

    async def handle_message(self):
        try:
            while not self._is_close:
                data = await self.receive_message()
                if not data:
                    break
                message = self.codec.decode(data)
                self.update_active_time()
            self.close()
        except Exception as error:
            logger.error(f"handle_message_error: {error}")
            self.close()

    async def receive_message(self) -> Optional[bytes]:
        while not self._is_close:
            message = self.buffer.receive_data()
            if message:
                return message
            data = await self.reader.read(1024)
            if not data:
                return None
            self.buffer.add_data(data)

    async def send_message(self, message: str):
        data = self.codec.encode(message)
        self.writer.write(data)
        # await self.writer.drain()
