from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🍽Menu', callback_data='menu')],
        [
            InlineKeyboardButton(text='Biz haqimizda', callback_data='aboutwe'),
            InlineKeyboardButton(text='Sozlamalar', callback_data='sozlamalar')
        ],
        [InlineKeyboardButton(text='Joy zakar qilish', callback_data='bronqilish')]
    ]
)

menu_admin_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Hot Dog', callback_data='hotdog'),
            InlineKeyboardButton(text='Pizza', callback_data='pizza')
        ],
        [
            InlineKeyboardButton(text='Gamburger', callback_data='gamburger'),
            InlineKeyboardButton(text='Donar', callback_data='donar')
        ],
        [
            InlineKeyboardButton(text='Lavash', callback_data='lavash'),
            InlineKeyboardButton(text='KFC', callback_data='kfc')
        ]
    ]
)

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Yangiliklar', callback_data='news')],
        [
            InlineKeyboardButton(text='Hot Dog', callback_data='hotdog'),
            InlineKeyboardButton(text='Pizza', callback_data='pizza')
        ],
        [
            InlineKeyboardButton(text='Gamburger', callback_data='gamburger'),
            InlineKeyboardButton(text='Donar', callback_data='donar')
        ],
        [
            InlineKeyboardButton(text='Lavash', callback_data='lavash'),
            InlineKeyboardButton(text='KFC', callback_data='kfc')
        ],
        [InlineKeyboardButton(text='Asosiy Menyu', callback_data='asosiymenyu')]
    ]
)

back_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Orqaga qaytish', callback_data='back')]
    ]
)

asosiymenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Asosiy Menyu', callback_data='asosiymenyu')]
    ]
)

nextorprevious = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='⬅️', callback_data='previous'), InlineKeyboardButton(text='➡️', callback_data='next')],
        [InlineKeyboardButton(text="Savatga qo'shish📥", callback_data='savesavat')],
        [InlineKeyboardButton(text='Savat🛒', callback_data='savat')]
    ]
)

plusminus = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='➖', callback_data='decrease'), InlineKeyboardButton(text='➕', callback_data='increase')],
        [InlineKeyboardButton(text="Tayyor✅", callback_data='tayyor')]
    ]
)