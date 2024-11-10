from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram import F
from loader import router_user, bot, db_pro, db_news
from keyboards.inline.main import main_menu, menu, back_menu, plusminus, savat, asosiymenu, create_product_keyboard, create_cart_button
from keyboards.default.main import buyurtmani_tugatish, dastavka, tolov, tel, location_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from product.delivery_option import FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING

class User(StatesGroup):
    phone = State()
    address = State()
    tolovturi = State()

ADMIN = 5471452269

@router_user.message(CommandStart())
async def start(msg: Message):
    await msg.answer('Asosiy Menu🏠:', reply_markup=main_menu)

# ------------------------------------ Asosiy Menu --------------------------------------
@router_user.callback_query(F.data == 'menu')
async def elektronikas(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Menu:", reply_markup=menu)

@router_user.callback_query(F.data == 'news')
async def show_news(callback: CallbackQuery):
    await callback.message.delete()
    news_list = db_news.get_all_news()  

    if news_list:  
        for _, title, description, image, _ in news_list:  
            await callback.message.answer_photo(photo=image, caption=f"<b>{title}</b>\n\n{description}", reply_markup=back_menu)
    else:
        await callback.message.answer("Yangiliklar topilmadi.") 


@router_user.callback_query(F.data.in_({"hotdog", "pizza", "gamburger", "donar", "lavash", "kfc"}))
async def show_hotdog_products(callback: CallbackQuery):
    await callback.message.delete()

    products = db_pro.get_products_by_category(callback.data)
    pro_name = (callback.data).capitalize()

    if products:
        inline_kb = create_product_keyboard(products)
        await callback.message.answer(f"{pro_name} kategoriyasidagi mahsulotlar:", reply_markup=inline_kb)
    else:
        await callback.answer(f"{pro_name} kategoriyasida mahsulotlar mavjud emas.", show_alert=True)
    await callback.answer()

@router_user.callback_query(lambda c: c.data.startswith("product_"))
async def show_product_detail(callback: CallbackQuery):
    await callback.message.delete() 
    product_id = int(callback.data.split("_")[1])
    product = db_pro.select_product_by_id(product_id)
    print(product_id)
    
    if product:
        productname = product[1]
        productprice = product[2]
        productdescription = product[3]
        productimage = product[4]
        await bot.send_photo(
            callback.from_user.id, 
            photo=productimage, 
            caption=f"Mahsulot nomi: {productname}\nMahsulot narxi: {productprice} so'm\nMahsulot tavsifi: {productdescription}", 
            reply_markup=create_cart_button(product_id)  
        )
    else:
        await callback.answer("Bu mahsulot topilmadi.", show_alert=True)

@router_user.callback_query(lambda c: c.data.startswith("savesavat_"))
async def add_to_cart(callback: CallbackQuery):
    try:
        product_id = int(callback.data.split("_")[1])
        product = db_pro.select_product_by_id(product_id)
        
        if product:
            db_pro.add_to_cart(db_pro.shopping_carts, callback.from_user.id, product_id)
            await callback.answer(f"{product[1]} savatga qo'shildi!", show_alert=False)
        else:
            await callback.answer("Mahsulot topilmadi.", show_alert=True)
    
    except ValueError:
        await callback.answer("Mahsulot ID noto'g'ri formatda kiritilgan.", show_alert=True)


@router_user.callback_query(lambda c: c.data == 'savat')
async def show_cart(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    cart_text = db_pro.show_cart(user_id)  

    if "bo'sh" not in cart_text:
        total = sum(
            int(line.split('=')[-1].strip().split()[0]) for line in cart_text.split('\n') if '=' in line
        )
        cart_text += f"\n\n<b>Jami:</b> {total} so'm"

        if callback_query.message.text:
            await callback_query.message.edit_text(text=cart_text, reply_markup=plusminus)
        else:
            await callback_query.message.answer(text=cart_text, reply_markup=plusminus)
    else:
        await callback_query.answer("Sizning savatingiz bo'sh.", show_alert=True)


@router_user.callback_query(lambda c: c.data == 'increase')
async def increase_quantity(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    product_id = int(callback_query.message.text.split(":")[1].strip().split()[0]) 
    db_pro.add_to_cart(db_pro.shopping_carts, user_id, product_id, quantity=1)
    await callback_query.answer("Miqdor oshirildi")
    await show_cart(callback_query)


@router_user.callback_query(lambda c: c.data == 'decrease')
async def decrease_quantity(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    product_id = int(callback_query.message.text.split(":")[1].strip().split()[0])  
    db_pro.remove_from_cart(db_pro.shopping_carts, user_id, product_id, quantity=1)
    await callback_query.answer("Miqdor kamaytirildi")
    await show_cart(callback_query)



async def show_cart_details(callback_query: CallbackQuery, user_id: int):
    cart = db_pro.show_cart(user_id)
    if cart != "Sizning savatingiz bo'sh.":
        total = sum(
            int(line.split('=')[-1].strip()) for line in cart.split('\n') if '=' in line
        )
        cart += f"\nJami: {total} so'm"
        if callback_query.message.photo:
            await callback_query.message.edit_caption(caption=cart, reply_markup=plusminus)
        else:
            await callback_query.message.edit_text(text=cart, reply_markup=plusminus)
    else:
        await callback_query.answer("Sizning savatingiz bo'sh.", show_alert=True)



@router_user.callback_query(lambda c: c.data == 'tayyor')
async def finish_order(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    cart = db_pro.show_cart(user_id)
    print(cart)
    if cart != "Sizning savatingiz bo'sh.":
        await bot.send_message(chat_id=user_id, text="Buyurtmangiz muvaffaqiyatli qabul qilindi. ", reply_markup=buyurtmani_tugatish)
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
    await state.set_state(User.tolovturi)
    await msg.answer("To'lov turini tanlang", reply_markup=tolov)

@router_user.message(User.tolovturi)
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

Agar siz Chustga borsangiz va tez tayyorlanadigan mazali taomlardan bahramand bo‘lishni istasangiz, Sug'diyona restoraniga albatta tashrif buyurishingizni tavsiya qilamiz!""", reply_markup=asosiymenu)

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