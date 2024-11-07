import asyncio
import logging
import sys

from loader import dp, bot, db_news, db_pro
import handlers

async def main():
    await dp.start_polling(bot)
    db_pro.close()
    db_news.close()
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())