from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Filter
from aiogram import F
from loader import router_admin
from keyboards.default.main import *
from keyboards.inline.main import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.news_db import *
from database.product_db import *

ADMIN = 5471452269

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

class Delete_Pro_ID(StatesGroup):
    id = State()

class Delere_New_ID(StatesGroup):
    id = State()

class Admin(Filter):
    def __init__(self, my_id: int):
        self.my_id = my_id

    async def __call__(self, msg: Message):
        return msg.from_user.id == self.my_id

@router_admin.message(CommandStart(), Admin(ADMIN))
async def start(msg: Message):
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
async def choice_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category=callback.data)

    # Ma'lumotlarni olish
    data = await state.get_data()
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    
    await state.clear() 
    await add_product(name, price, description, image, category)
    
    await callback.message.answer("Mahsulot qo'shildi!") 

# ------------------------------------------ Delete products ------------------------------------------
@router_admin.message(F.text == "Mahsulot o'chirish", Admin(ADMIN))
async def view_products(msg: Message, state: FSMContext):
    products = await get_all_products()  # Barcha mahsulotlarni olish
    if products:
        # Takrorlangan mahsulotlarni olib tashlash
        unique_products = {product['id']: product for product in products}.values()

        # Mahsulotlarni formatlash
        product_list = "\n".join(
            [f"{product['id']}. {product['name']} - {product['price']} so'm" for product in unique_products]
        )
        await msg.answer(f"Mahsulotlar:\n{product_list}\nO'chirish uchun mahsulot ID sini kiriting:")
        await state.set_state(Delete_Pro_ID.id)
    else:
        await msg.answer("Hech qanday mahsulot topilmadi.")

@router_admin.message(Delete_Pro_ID.id, Admin(ADMIN))
async def delete_product_handler(msg: Message, state: FSMContext):
    try:
        # Foydalanuvchining ID sini integerga o‘tkazish
        product_id = int(msg.text)

        # Ma'lumotlar bazasidan mahsulotni o'chirish
        success = await delete_product(product_id)

        if success:
            await msg.answer("Mahsulot muvaffaqiyatli o'chirildi!")
        else:
            await msg.answer("Bunday ID li mahsulot topilmadi.")
    except ValueError:
        # Agar foydalanuvchi noto‘g‘ri qiymat kiritsa
        await msg.answer("Iltimos, faqat mahsulot ID sini kiriting!")
    except Exception as e:
        # Boshqa xatoliklar uchun
        await msg.answer(f"Xatolik yuz berdi: {e}")
    finally:
        # Holatni tugatish
        await state.clear()



# ------------------------------------------ View all products ------------------------------------------
@router_admin.message(F.text == "Barcha mahsulotlarni ko'rish", Admin(ADMIN))
async def view_all_products(msg: Message):
    products = await get_all_products()  # Barcha mahsulotlarni olish
    if products:
        product_list = "\n".join(
            [f"{p['id']}. {p['name']} - {p['price']} so'm" for p in products]
        )
        await msg.answer(f"Barcha mahsulotlar:\n{product_list}", reply_markup=products_key_admin)
    else:
        await msg.answer("Hech qanday mahsulot topilmadi.")

# ---------------------------------------------- News Add ---------------------------------------------------
@router_admin.message(F.text == "Yangilik qo'shish", Admin(ADMIN))
async def add_news(msg: Message, state: FSMContext):
    # Retrieve all existing news
    news_items = await get_all_news()  # Yangiliklarni olish
    if news_items:
        news_list = "\n".join([f"{n[0]}. {n[1]} - {n[2]}" for n in news_items])
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

    await add_newss(title, description, image)
    await state.clear() 
    
    await msg.answer("Yangilik qo'shildi!")

# ------------------------------------------ News Delete ------------------------------------------------
@router_admin.message(F.text == "Yangilik o'chirish", Admin(ADMIN))
async def add_news(msg: Message, state: FSMContext):
    # Retrieve all existing news
    news_items = await get_all_news()  # Yangiliklarni olish
    if news_items:
        news_list = "\n".join([f"{n[0]}. {n[1]} - {n[2]}" for n in news_items])
        await msg.answer(f"Mavjud yangiliklar:\n{news_list}\n\nO'chirmoqchi bo'lgan yangilik ID sini kiriting:")
        await state.set_state(Delere_New_ID.id)
    else:
        await msg.answer('Hech qanday yangilik topilmadi.\nYangi yangilikning sarlavhasini kiriting:')

@router_admin.message(Delere_New_ID.id, Admin(ADMIN))
async def delete_new(msg: Message, state: FSMContext):
    await state.update_data(id = msg.text)
    try:
        news_id = int(msg.text)
        success = await delete_product(news_id)

        if success:
            await msg.answer("Yangilik muvaffaqiyatli o'chirildi!")
        else:
            await msg.answer("Bunday ID li yangilik topilmadi.")
    except ValueError:
        # Agar foydalanuvchi noto‘g‘ri qiymat kiritsa
        await msg.answer("Iltimos, faqat yangilik ID sini kiriting!")
    except Exception as e:
        # Boshqa xatoliklar uchun
        await msg.answer(f"Xatolik yuz berdi: {e}")
    finally:
        # Holatni tugatish
        await state.clear()
# ------------------------------------------ View all news -----------------------------------------------
@router_admin.message(F.text == "Barcha yangiliklarni ko'rish", Admin(ADMIN))
async def view_all_news(msg: Message):
    news = await get_all_news()

    if news:
        news_list = "\n\n".join(
            [
                f"📌 **{n[1]}**\n📝 {n[2]}\n🕒 {n[4]}"
                for n in news
            ]
        )
        await msg.answer(f"Barcha yangiliklar:\n\n{news_list}", reply_markup=news_key_admin)
    else:
        await msg.answer("Hech qanday yangilik topilmadi!")


# -------------------------------------------- Back Menu --------------------------------------------

@router_admin.message(F.text == 'Ortga qaytish')
async def back_menu_admin(msg: Message):
    await msg.answer("Menyuga qaytdingiz!", reply_markup = menu_admin_default)