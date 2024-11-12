from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Filter, Command
from aiogram import F
from loader import router_admin, bot, db_pro, db_news
from keyboards.default.main import menu_admin_default
from keyboards.inline.main import menu_admin_inline
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN

class Product(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()
    category = State()

class News(StatesGroup):
    title = State()
    description = State()
    image = State()

class Admin(Filter):
    def __init__(self, my_id: int):
        self.my_id = my_id

    async def __call__(self, msg: Message):
        return msg.from_user.id == self.my_id

@router_admin.message(CommandStart(), Admin(ADMIN))
async def start(msg: Message):
    db_pro.create_table()
    await msg.answer('Assalomu aleykum Admin!', reply_markup=menu_admin_default)

# ------------------------------------- Add new food item --------------------------------
@router_admin.message(F.text == "Yangi mahsulot qo'shish", Admin(ADMIN))
async def add_food(msg: Message, state: FSMContext):
    await state.set_state(Product.name)
    await msg.answer('Mahsulotning nomini kiriting:')

@router_admin.message(Product.name, Admin(ADMIN))
async def set_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await state.set_state(Product.description)
    await msg.answer('Mahsulotning tavsifini kiriting:')

@router_admin.message(Product.description, Admin(ADMIN))
async def set_description(msg: Message, state: FSMContext):
    await state.update_data(description=msg.text)
    await state.set_state(Product.price)
    await msg.answer('Mahsulotning narxini kiriting:')

@router_admin.message(Product.price, Admin(ADMIN))
async def set_price(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer("Iltimos, to'g'ri narxni kiriting (raqam):")
        return
    await state.update_data(price=float(msg.text))  # Narxni floatga o'tkazamiz
    await state.set_state(Product.image)
    await msg.answer('Mahsulotning rasmini yuboring:')

@router_admin.message(Product.image, F.photo, Admin(ADMIN))
async def productimage_set(msg: Message, state: FSMContext):
    photo_id = msg.photo[-1].file_id
    await state.update_data(image=photo_id)
    await state.set_state(Product.category)
    await msg.answer('Mahsulotning kategoriyasini tanlang:', reply_markup=menu_admin_inline)

# ------------------------------------- Enter mahsulot categories --------------------------------
@router_admin.callback_query(F.data.in_({"hotdog", "pizza", "gamburger", "donar", "lavash", "kfc"}), Product.category, Admin(ADMIN))
async def add_product(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category=callback.data)

    data = await state.get_data()
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    
    await state.clear() 
    db_pro.add_products(name, price, description, image, category)
    
    await callback.message.answer("Mahsulot qo'shildi!") 

# ------------------------------------------ Delete products ------------------------------------------
@router_admin.message(F.text == "Mahsulot o'chirish", Admin(ADMIN))
async def view_products(msg: Message):
    products = db_pro.get_all_products()  
    if products:
        product_list = "\n".join([f"{p[0]}. {p[1]} - {p[2]} so'm" for p in products])
        await msg.answer(f"Mahsulotlar:\n{product_list}\nO'chirish uchun mahsulot ID sini kiriting:")
    else:
        await msg.answer("Hech qanday mahsulot topilmadi.")

@router_admin.message(F.text.isdigit(), Admin(ADMIN))
async def delete_product(msg: Message):
    product_id = int(msg.text)
    success = db_pro.delete_product(product_id)  
    if success:
        await msg.answer("Mahsulot muvaffaqiyatli o'chirildi!")
    else:
        await msg.answer("Mahsulotni o'chirishda xato yuz berdi. Iltimos, ID ni tekshiring.")

# ---------------------------------------------- News Add ---------------------------------------------------
@router_admin.message(F.text == "Yangilik qo'shish", Admin(ADMIN))
async def add_news(msg: Message, state: FSMContext):
    # Retrieve all existing news
    news_items = db_news.get_all_news() 
    if news_items:
        news_list = "\n".join([f"{n[0]}. {n[1]} - {n[2]} - created time: {n[4]}" for n in news_items])
        await msg.answer(f"Mavjud yangiliklar:\n{news_list}\n\nYangi yangilikning sarlavhasini kiriting:")
    else:
        await msg.answer('Hech qanday yangilik topilmadi.\nYangi yangilikning sarlavhasini kiriting:')

    await state.set_state(News.title)

@router_admin.message(News.title, Admin(ADMIN))
async def set_news_title(msg: Message, state: FSMContext):
    await state.update_data(title=msg.text)
    await state.set_state(News.description)
    await msg.answer('Yangilikning tavsifini kiriting:')

@router_admin.message(News.description, Admin(ADMIN))
async def set_news_description(msg: Message, state: FSMContext):
    await state.update_data(description=msg.text)
    await state.set_state(News.image)
    await msg.answer('Yangilikning rasmini yuboring:')

@router_admin.message(News.image, F.photo, Admin(ADMIN))
async def news_image_set(msg: Message, state: FSMContext):
    photo_id = msg.photo[-1].file_id
    await state.update_data(image=photo_id)

    data = await state.get_data()
    title = data['title']
    description = data['description']
    image = data['image']
    
    await state.clear() 
    db_news.add_news(title, description, image)
    
    await msg.answer("Yangilik qo'shildi!")

# ------------------------------------------ View all products ------------------------------------------
@router_admin.message(F.text == "Barcha mahsulotlarni ko'rish", Admin(ADMIN))
async def view_all_products(msg: Message):
    products = db_pro.get_all_products() 
    if products:
        product_list = "\n".join([f"{p[0]}. {p[1]} - {p[2]} so'm" for p in products])
        await msg.answer(f"Barcha mahsulotlar:\n{product_list}")
    else:
        await msg.answer("Hech qanday mahsulot topilmadi.")