from aiogram import Dispatcher, Router, Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from database.product_db import Database_Product
from database.news_db import Database_News
from config import TOKEN

db_pro = Database_Product()
db_news = Database_News()
dp = Dispatcher()
router_admin = Router()
router_user = Router()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp.include_router(router=router_admin)
dp.include_router(router=router_user)
