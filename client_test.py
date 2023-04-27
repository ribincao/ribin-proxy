from logger import logger
import asyncio


TEST_CLIENT_PORT = 8088


async def test_client():
    _, writer = await asyncio.open_connection("localhost", TEST_CLIENT_PORT)
    try:
        while True:
            data = b"hello"
            logger.info(f"Test Send {data}")
            writer.write(data)
            await asyncio.sleep(1)
    except Exception as error:
        logger.error(f"{error}")
        writer.close()


if __name__ == '__main__':
    logger.init_logger()
    loop = asyncio.get_event_loop()
    loop.create_task(test_client())
    loop.run_forever()


