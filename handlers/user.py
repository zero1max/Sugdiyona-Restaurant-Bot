from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from keyboards.default.main import buyurtmani_tugatish, dastavka, tolov, tel, location_keyboard
from keyboards.inline.main import main_menu, menu, back_menu, plusminus, asosiymenu, create_product_keyboard, \
    create_cart_button
from loader import router_user, bot
from config import ADMIN
from database.news_db import get_all_news
from database.product_db import *


class User(StatesGroup):
    phone = State()
    address = State()
    payment_type = State()


@router_user.message(CommandStart())
async def start(msg: Message):
    await set
    await msg.answer('Asosiy Menu🏠:', reply_markup=main_menu) # noqa


# ------------------------------------ Main Menu --------------------------------------
@router_user.callback_query(F.data == 'menu')
async def elektronikas(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Menu:", reply_markup=menu)


@router_user.callback_query(F.data == 'news')
async def show_news(callback: CallbackQuery):
    await callback.message.delete()
    news_list = await get_all_news()

    if news_list:
        for _, title, description, image, _ in news_list:
            await callback.message.answer_photo(photo=image, caption=f"<b>{title}</b>\n\n{description}",
                                                reply_markup=back_menu)
    else:
        await callback.message.answer("Yangiliklar topilmadi.") # noqa

# ------------------------------------Menu -------------------------------------------------------------

@router_user.callback_query(F.data.in_({"hotdog", "pizza", "gamburger", "donar", "lavash", "kfc"})) # noqa
async def show_hotdog_products(callback: CallbackQuery):
    await callback.message.delete()

    products = await get_products_by_category(callback.data)
    pro_name = (callback.data).capitalize()

    if products:
        inline_kb = create_product_keyboard(products)
        await callback.message.answer(f"{pro_name} kategoriyasidagi mahsulotlar:", reply_markup=inline_kb) # noqa
    else:
        await callback.answer(f"{pro_name} kategoriyasida mahsulotlar mavjud emas.", show_alert=True) # noqa
    await callback.answer()


@router_user.callback_query(lambda c: c.data.startswith("product_"))
async def show_product_detail(callback: CallbackQuery):
    await callback.message.delete()
    product_id = int(callback.data.split("_")[1])
    product = await select_product_by_id(product_id)
    if product:
        product_name, product_price, product_description, product_image = product[1:5]
        await bot.send_photo(
            callback.from_user.id,
            photo=product_image,
            caption=f"Mahsulot nomi: {product_name}\nNarxi: {product_price} so'm\nTavsifi: {product_description}", # noqa
            reply_markup=create_cart_button(product_id)  
        )
    else:
        await callback.answer("Bu mahsulot topilmadi.", show_alert=True) # noqa


@router_user.callback_query(lambda c: c.data.startswith("savesavat_")) # noqa
async def add_to_cart(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    product = await select_product_by_id(product_id)
    if product:
        await add_to_cart(callback.from_user.id, product_id)
        await callback.answer(f"{product[1]} savatga qo'shildi!", show_alert=False) # noqa
    else:
        await callback.answer("Mahsulot topilmadi.", show_alert=True) # noqa


@router_user.callback_query(lambda c: c.data == 'savat') # noqa
async def show_cart(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    cart_text, total_price = await show_cart(user_id)
    print(cart_text)
    print(cart_text[-1])
    print(cart_text[-6])
    print(total_price)

    if cart_text:
        cart_message = f"<b>Sizning savatingizdagi mahsulotlar:</b>\n\n{cart_text}\n\n<b>Jami:</b> {total_price} so'm \n count:{cart_text[-6]}" # noqa
        if callback_query.message.text:
            await callback_query.message.edit_text(text=cart_message, reply_markup=plusminus)
        else:
            await callback_query.message.answer(text=cart_message, reply_markup=plusminus)
    else:
        await callback_query.answer("Sizning savatingiz bo'sh.", show_alert=True) # noqa


@router_user.callback_query(lambda c: c.data.startswith('increase'))
async def increase_quantity(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    cart_text, total_price = await show_cart(user_id)
    await increment_product_count(cart_text[-1])
    await callback_query.answer("Miqdor oshirildi") # noqa
    await show_cart(callback_query)



@router_user.callback_query(lambda c: c.data == 'tayyor')
async def finish_order(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    cart = await show_cart(user_id)

    if cart != "Sizning savatingiz bo'sh.":
        await bot.send_message(chat_id=user_id, text="Buyurtmangiz muvaffaqiyatli qabul qilindi.",
                               reply_markup=buyurtmani_tugatish)
        await callback_query.message.delete()
        await callback_query.answer("Buyurtma qabul qilindi")
    else:
        await callback_query.answer("Savatingiz bo'sh.", show_alert=True)


@router_user.message(F.text == "Buyurtmani tugatish")
async def choice_dastavka(msg: Message):
    await msg.answer("Buyurtma turini tanlang", reply_markup=dastavka)


# ------------------------------------------- Eltib berish --------------------------------
@router_user.message(F.text == "Eltib berish")
async def eltibberish(msg: Message, state: FSMContext):
    await state.set_state(User.phone)
    await msg.answer("Telefon raqamingizni kiriting:", reply_markup=tel)


@router_user.message(User.phone, F.contact)
async def get_phone(msg: Message, state: FSMContext):
    if msg.contact:
        contact = msg.contact.phone_number
    else:
        contact = msg.text
    await state.update_data(phone=contact)
    await state.set_state(User.address)
    await msg.answer("Manzilingizni yuboring!", reply_markup=location_keyboard)


@router_user.message(User.address)
async def get_address(msg: Message, state: FSMContext):
    if msg.location:
        location = {'latitude': msg.location.latitude, 'longitude': msg.location.longitude}
    else:
        location = msg.text

    await state.update_data(address=location)
    await state.set_state(User.payment_type)
    await msg.answer("To'lov turini tanlang", reply_markup=tolov)


@router_user.message(User.payment_type)
async def get_tolovturi(msg: Message, state: FSMContext):
    tolovturi = msg.text
    await state.update_data(tolovturi=tolovturi)
    data = await state.get_data()

    phone = data.get('phone')
    address = data.get('address')
    tolovturi = data.get('tolovturi')

    message_text = f"Yangi buyurtma:\nTelefon raqami: {phone}\nTo'lov turi: {tolovturi}"
    await bot.send_message(chat_id=ADMIN, text=message_text)

    if isinstance(address, dict) and 'latitude' in address and 'longitude' in address:
        await bot.send_location(chat_id=ADMIN, latitude=address['latitude'], longitude=address['longitude'])

    await msg.answer("Rahmat! Ma'lumotlaringiz qabul qilindi.", reply_markup=asosiymenu)


# ----------------------------------------- Borib olish ---------------------------------
@router_user.message(F.text == 'Borib olish')
async def boribolish(msg: Message):
    latitude = 41.23437586925201
    longitude = 69.21561572492116
    await bot.send_location(msg.from_user.id, latitude=latitude, longitude=longitude)
    await bot.send_contact(
        chat_id=msg.from_user.id,
        phone_number='+9989404733207',
        first_name="Sug'diyona Restorani")
    await msg.answer("Biz bilan bog'lanish uchun telefon raqam va manzilimiz!", reply_markup=asosiymenu)


# ------------------------------------ About We -----------------------------------------
@router_user.callback_query(F.data == 'aboutwe')
async def elektronikas(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("""Sug'diyona Restorani

Namangan viloyatining Chust shahrida joylashgan Sug'diyona restorani mahalliy aholi va mehmonlar orasida mashhur maskan hisoblanadi. Restoran asosan turli xil fast food taomlarini taklif qiladi. Bu yerda burger, hot-dog, kartoshka fri va boshqa zamonaviy tez tayyorlanadigan taomlarni topish mumkin.

Restoran ichki interyeri zamonaviy uslubda bezatilgan bo‘lib, qulay va osoyishta muhit yaratishga harakat qilingan. Sug'diyona oila a’zolari va do‘stlar bilan vaqt o‘tkazish uchun ajoyib joy. Tez xizmat ko‘rsatish, mazali taomlar va o‘rtacha narxlar bu joyni yanada jozibador qiladi.

Agar siz Chustga borsangiz va tez tayyorlanadigan mazali taomlardan bahramand bo‘lishni istasangiz, Sug'diyona restoraniga albatta tashrif buyurishingizni tavsiya qilamiz!""",
                                  reply_markup=asosiymenu)


# ------------------------------------ Sozlamalar -----------------------------------------
@router_user.callback_query(F.data == 'sozlamalar')
async def elektronikas(callback: CallbackQuery):
    await callback.message.delete()


# ------------------------------------ Bronqilish -----------------------------------------
@router_user.callback_query(F.data == 'bronqilish')
async def elektronikas(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Joy zakaz qilish uchun pastdagi telefon raqamga aloqaga chiqing!"
    )
    await bot.send_contact(
        chat_id=callback.from_user.id,
        phone_number='+9989404733207',
        first_name="Sug'diyona Restorani",
        reply_markup=asosiymenu
    )


# ------------------------------------ Menu ga qaytish -----------------------------------------
@router_user.callback_query(F.data == 'back')
async def back(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Menu:", reply_markup=menu)


# ------------------------------------ Asosiy Menu ga qaytish -----------------------------------------
@router_user.callback_query(F.data == 'asosiymenyu')
async def back(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Asosiy Menu:", reply_markup=main_menu)


# --------------------------------------- I Don't Know -----------------------------------
@router_user.message()
async def start(msg: Message):
    await msg.answer("Chunmadim")
