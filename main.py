import asyncio
import logging
import sys

from database.news_db import setup_db
from loader import dp, bot, db_pro
import handlers

async def main():
    await setup_db()
    await dp.start_polling(bot)
    db_pro.close()

    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())