import asyncio
from proxy import Proxy
from .logger import logger


class Server(object):
    SERVER_PORT = 8888

    def __init__(self):
        self._loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self._proxy: Proxy = Proxy(self.SERVER_PORT)

    def run(self):
        self._loop.create_task(self._proxy.run_server())
        self._loop.run_forever()


if __name__ == '__main__':
    logger.init_logger()
    server = Server()
    server.run()
