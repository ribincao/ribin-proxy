import asyncio
from proxy import Proxy
from logger import logger


class Client(object):

    def __init__(self):
        self._loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self._proxy: Proxy = Proxy(8088)

    def run(self):
        self._loop.create_task(self._proxy.run_client())
        self._loop.run_forever()


if __name__ == '__main__':
    logger.init_logger()
    client = Client()
    client.run()
