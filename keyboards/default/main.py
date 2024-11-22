from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_admin_default = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="Barcha mahsulotlarni ko'rish")],
        [KeyboardButton(text="Barcha yangiliklarni ko'rish")]
    ]
)

products_key_admin = ReplyKeyboardMarkup(
    resize_keyboard = True,
    keyboard=[
        [KeyboardButton(text="Yangi mahsulot qo'shish"), KeyboardButton(text="Mahsulot o'chirish")],
        [KeyboardButton(text="Ortga qaytish")]
    ]
)

news_key_admin = ReplyKeyboardMarkup(
    resize_keyboard = True,
    keyboard=[
        [KeyboardButton(text="Yangilik qo'shish"), KeyboardButton(text="Yangilik o'chirish")],
        [KeyboardButton(text="Ortga qaytish")]
    ]
)

back_key_admin = ReplyKeyboardMarkup(
    resize_keyboard = True,
    keyboard=[
        [KeyboardButton(text="Ortga qaytish")]
    ]
)

buyurtmani_tugatish = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Buyurtmani tugatish')]
    ]
)

dastavka = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Eltib berish'), KeyboardButton(text='Borib olish')]
    ]
)

tolov = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Naqd pul'), KeyboardButton(text='Click')]
    ]
)

tel = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Telefon raqamingizni jo'nating!",
    keyboard=[
        [KeyboardButton(text="Telefon raqam jo'natish📱", request_contact=True)]
    ]
)

location_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Manzilingizni jo'nating!",
    keyboard=[
        [KeyboardButton(text="Manzilni jo'natish📍", request_location=True)]
    ]
)