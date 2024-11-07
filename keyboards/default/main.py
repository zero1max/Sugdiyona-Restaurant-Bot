from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_admin_default = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="Yangi mahsulot qo'shish"), KeyboardButton(text="Yangilik qo'shish")],
        [KeyboardButton(text="Mahsulot o'chirish"), KeyboardButton(text="Barcha mahsulotlarni ko'rish")]
    ]
)

buyurtmani_tugatish = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Buyurtmani tugatish')]
    ]
)