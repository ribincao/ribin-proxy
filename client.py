import asyncio
from proxy import Proxy


class Client(object):

    def __init__(self):
        self._loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self._proxy: Proxy = Proxy(8888)

    def run(self):
        self._loop.create_task(self._proxy.run_client())
        self._loop.run_forever()


if __name__ == '__main__':
    client = Client()
    client.run()
