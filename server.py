import asyncio
from proxy import Proxy


class Server(object):

    def __init__(self):
        self._loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self._proxy: Proxy = Proxy(8888)

    def run(self):
        self._loop.create_task(self._proxy.run_server())
        self._loop.run_forever()


if __name__ == '__main__':
    server = Server()
    server.run()
