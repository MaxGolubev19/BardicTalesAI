import sys
import asyncio
import logging

from bot import GameBot

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    stream=open('info/log.txt', 'a'))


async def main():
    bot = GameBot()
    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())
