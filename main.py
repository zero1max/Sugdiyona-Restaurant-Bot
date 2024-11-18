import asyncio
import logging
import sys

from database.news_db import setup_db
from database.product_db import setup
from loader import dp, bot
import handlers

async def main():
    await setup_db()
    await setup()
    await dp.start_polling(bot)

    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())