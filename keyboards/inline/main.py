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

savat = InlineKeyboardMarkup(
    inline_keyboard=[
        # [InlineKeyboardButton(text='⬅️', callback_data='previous'), InlineKeyboardButton(text='➡️', callback_data='next')],
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

def create_product_keyboard(products):
    # InlineKeyboardButton ob'ektlarini saqlash uchun ro'yxat yaratamiz
    buttons = []
    row = []  # Mahsulotlar tugmalarini juft bo'lib saqlash uchun vaqtinchalik ro'yxat

    for index, product in enumerate(products):
        # Har bir mahsulot uchun tugma yaratamiz
        button = InlineKeyboardButton(
            text=f"{product[1]}", 
            callback_data=f"product_{product[0]}"
        )
        row.append(button)

        # Agar juft mahsulot bo'lsa yoki oxirgi elementga yetgan bo'lsak, qatorni `buttons` ga qo'shamiz
        if len(row) == 2 or index == len(products) - 1:
            buttons.append(row)
            row = []  # Yangi qatorni yaratish uchun ro'yxatni tozalaymiz

    if products:
        back_button = [InlineKeyboardButton(text='Orqaga qaytish', callback_data='back')]
        buttons.append(back_button)

    # InlineKeyboardMarkup yaratamiz
    inline_kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_kb

def create_cart_button(product_id):
    # Create InlineKeyboardButton with the correct callback_data
    button = InlineKeyboardButton(text="Savatchaga qo'shish", callback_data=f"savesavat_{product_id}")
    button1 = InlineKeyboardButton(text='Savat🛒', callback_data='savat')
    
    # Create InlineKeyboardMarkup and add the button in a list
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button], [button1]])
    
    return keyboard
