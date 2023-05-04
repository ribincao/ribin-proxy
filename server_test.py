import asyncio
from .logger import logger


TEST_SERVER_PORT = 8888

async def test_server():
    async def test_call_back(local_reader: asyncio.StreamReader, local_writer: asyncio.StreamWriter):
        logger.info(f"[TestServer] Connected.")
        while True:
            data = await local_reader.read(1024)
            if not data:
                break
            logger.info(f"Test Server Receive {data}")
        local_writer.close()
        logger.info(f"Connection Closed.")

    server = await asyncio.start_server(test_call_back, port=TEST_SERVER_PORT)
    logger.info(f"Test ShadowSocks Server started on {server.sockets[0].getsockname()}")
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    logger.init_logger()
    loop = asyncio.get_event_loop()
    loop.create_task(test_server())
    loop.run_forever()

