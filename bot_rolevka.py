from os import getenv
from dotenv import load_dotenv

import logging
import asyncio

from handlers import *

from models.character import *
from models.inventory import *
from models.level import *
from models.player import *
from photosk import *

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.state import State, StatesGroup

# Включаем логирование
logging.basicConfig(
    level=logging.DEBUG, 
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s", 
    datefmt='%H:%M:%S',
    )


# Загружаем переменные окружения из .env файла
load_dotenv('hook.env')

# ПРИСВАИВАНИЕ
logging.basicConfig(level=logging.INFO)
bot= Bot(token = getenv('API_TOKEN'))
stora = MemoryStorage()
dp = Dispatcher(storage=stora)
router = Router()

def get_character(user_id):
    return user_characters.get(user_id)
# КНОПКИ 
async def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text = 'О нас \U0001f4d6'), KeyboardButton( text = 'Начать игру \U0001f3b2')]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard= kb_list, 
        resize_keyboard= True,
        one_time_keyboard= True,
        input_field_placeholder= 'Воспользуйтесь меню:'
        )
    return keyboard

async def schop_kb(user_telegram_id: int):
    schop_list = [
        [KeyboardButton(text='Направиться в магазин \U0001f4b0')]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=schop_list,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard
    
async def play_kb(user_telegram_id: id):
    kb_play = [
        [KeyboardButton(text='Приготовиться к бою \u2694\uFE0F', callback_data = 'figth')],
        [KeyboardButton(text='Инвентарь \U0001f392', callback_data = 'inventa'), KeyboardButton(text='Скрыться \U0001f464', callback_data = 'stels')],
        [KeyboardButton(text='Изучить место \U0001f4dc', callback_data = 'info'), KeyboardButton(text='Особые умения \U0001f31f', callback_data = 'spell')]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_play,
        resize_keyboard= True
    )
    return keyboard

# ОСНОВНАЯ ЧАСТЬ
@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    logging.info(f"User {message.from_user.id}/{message.from_user.full_name} start game.")
    await message.reply('Добро пожаловать !\n\n Прежде чем мы начнем небольшое введение )\n\U0001f4aa - ваша сила, от нее зависит ваш урон. Когда вы пьете особые зелья, покупаете оружие и находите артефакты она растет.\n\U0001f6e1\uFE0F - ваша броня, чем она выше тем больше защиты у вас и меньше ловкости из-за ее веса\n\U0001f3c3 - ловкость, от нее зависит сможете ли вы уклониться от атаки и пройти особые испытания.\n\U0001f441\uFE0F\u200D\U0001f5e8\uFE0F - находчивость, она нужна для прохождения особых испытаний.\n\U0001f357 - голод, ваша естественная потребность в еде !\n\u2764\uFE0F - ваше здоровье\n\U0001f4a7 - это ваша мана, помните что она нужна только тем, кто умеет использовать заклинания !',
                         reply_markup= await main_kb(message.from_user.id))

user_characters = {}
# Словарь для хранения игроков


@dp.message(F.text == 'О нас \U0001f4d6')
async def info_group(message: types.Message):
    logging.info(f'User {message.from_user.id}/{message.from_user.full_name} get info about us!')
    await message.answer(f'Бот разработан по заказу: @Malaret \nРазрабочик:@dmitry_skn',
                         reply_markup=await main_kb(message.from_user.id))

players = {}

def get_player(user_id):
    return players.get(user_id)

@dp.message(F.text == 'Начать игру \U0001f3b2')
async def start_game(message: types.Message):
    logging.info
    rod = await message.answer_dice("\U0001f3b2")
    persona = rod.dice.value
    player = players.get(message.from_user.id, Player(message.from_user.id))
    players[message.from_user.id] = player

    if persona in range(1, 4) :
        hero = Character(name = 'Оливер', tipe= 'простой крестьянин', hp = 100, strength= 15, agility=70, hunger=10, perception=50, money= 10)
        intro = 'Вы родились в простой деревне, где каждый день был наполнен трудом на полях и заботой о семье. С раннего утра до позднего вечера вы работали, обрабатывая землю и ухаживая за скотом. Но в вашем сердце всегда жила мечта о лучшей жизни, о том, чтобы однажды покинуть пределы родного села и увидеть мир за его границами. Шли годы и вы продолжали жить как и прежде, но теперь, когда слухи о приключениях доходят до вашего уха, вы чувствуете, что пришло время покинуть привычный быт. Чтобы изменить свою судьбу и принести славу своей семье, вам нужно совершить подвиг, который изменит вашу жизнь навсегда. \n\nГоды жизни в вашей деревне сделали вас устойчивым к тяжелым и голодным временам, чувство голода меньше терзает вас'
    elif persona in range(4, 6):
        hero = Character(name= 'Ричард', tipe = 'рыцарь', hp=150 , strength= 20, agility=90, hunger=7, perception=55, money= 10)
        intro = 'Вы родились в благородной семье, где с раннего возраста вас учили искусству войны и кодексу чести. С детства вы наблюдали за подвигами великих рыцарей, их отвагой и благородством, и мечтали о том, чтобы однажды стать одним из них. Ваши тренировки были изнурительными, но вы никогда не жаловались — каждый удар меча и каждое занятие верховой ездой приближали вас к вашей мечте. С годами вы стали искусным воином, обладающим не только силой, но и мудростью. Вы знаете, что истинная доблесть заключается не только в мастерстве с оружием, но и в умении защищать слабых, проявлять сострадание и следовать кодексу чести. Однако, несмотря на все достижения, вы понимаете, что для того, чтобы стать полноценным рыцарем, вам необходимо совершить подвиг, который будет говорить о вашей доблести и преданности. Теперь, когда вы стоите на пороге своего судьбоносного приключения, ваше сердце полно решимости. Вы готовы отправиться в путь, чтобы сразиться с чудовищами, защитить невинных и завоевать славу, которая сделает вас легендой. Ваше имя будет звучать в песнях бардов, а ваши подвиги будут вдохновлять будущие поколения.\n\nВы сильны и здоровы, многочисленные тренировки укрепили ваше тело.'
    elif persona == 6:
        hero = Character(name= 'Моргана', tipe='волшебница', mana=350, hp= 90, strength= 15, agility=50, hunger=6, perception=70, money= 10)
        intro = 'Удача улыбнулась вам. С детсва вам была дарована сила, что отличала вас. Ваша жизнь была полна изучения древних текстов и практики магии, и вы провели годы, обучаясь у мудрых наставников. Каждое заклинание, которое вы произносили, приближало вас к пониманию тайн вселенной и вашей истинной природы. Теперь, когда вы достигли зрелости, вы готовы использовать свои знания и способности для великих дел. Ваша цель — не просто овладеть магией, но и стать защитницей слабых, исследовать неизведанные земли и раскрывать секреты, которые могут изменить ход истории. Чтобы заслужить уважение и признание, вам нужно совершить подвиг, который продемонстрирует силу вашей магии и вашу преданность делу. \nВы заглядываете в книгу волшебства: \n\nОгненный шар \U0001f525 - требует 20 маны и наносит средний урон\nЩит света \u2600\uFE0F - дарует немного защиты в обмен на 250 маны \nЦепная молния \u26A1 - наности средний урон нескольким врагам и потребляет 30 маны \nИсцеление \u2764\uFE0F - восстанавливает здоровье и потребляет 50 маны \nМетеор \U0001f4ab - это заклинание может нанести огромный урон нескольким врагам за 100 маны. \n\nПомните об этом, когда будете пользоваться своей силой.'

    await asyncio.sleep(6)
    user_characters[message.from_user.id] = hero    
    await message.answer(f"Игра началась! \U0001f389 \nВам выпало {rod.dice.value} \n{hero.character_info()}\n\n{intro}")
    await asyncio.sleep(2)
    await message.answer('Осталось запастись всем необходимым и выдвигаться, всего у вас 10 монет',
                        reply_markup= await schop_kb(message.from_user.id))
    return player



@dp.message(F.text == 'Направиться в магазин \U0001f4b0')
async def start_shop(message: types.Message):
    logger = logging.getLogger(__name__)
    logger.info(f"User {message.from_user.id}/{message.from_user.full_name} is going to the shop.")
    keyboard_shop = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Еда \U0001f35e', callback_data='shop_food'),
            InlineKeyboardButton(text='Оружие \u2694\uFE0F', callback_data='shop_weapons')
        ],
        [
            InlineKeyboardButton(text='Броня \U0001f6e1\uFE0F', callback_data='shop_armor'),
            InlineKeyboardButton(text='Зелья \U0001f9ea', callback_data='shop_potions')
        ],
        [
            InlineKeyboardButton(text='Устремиться вперед \U0001f3c3', callback_data='start_adventure')
        ]
    ])

    photo = FSInputFile(photo_1)  

    await bot.send_photo(chat_id=message.chat.id, 
    photo=photo, 
    caption=f'Куда вы направитесь ?',
    parse_mode="HTML", 
    reply_markup=keyboard_shop)
    
# Обработчик для выбора категории
@dp.callback_query(F.data == 'shop_food')
async def shop_food(callback: types.CallbackQuery):
    logging.info(f'User {callback.message.from_user.id}/{callback.message.from_user.full_name} shopping food')
    await callback.message.delete()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Сухари 1 \U0001fa99', callback_data='buy_krekers'),
            InlineKeyboardButton(text='Хлеб 2 \U0001fa99', callback_data='buy_bread')
        ],
        [
            InlineKeyboardButton(text='Мясо 3 \U0001fa99', callback_data='buy_meat'),
            InlineKeyboardButton(text='Назад \U0001f6aa', callback_data='back_to_shop')
        ]
    ])
    
    await callback.message.answer("Выберите еду:", reply_markup=keyboard)

@dp.callback_query(F.data == 'shop_weapons')
async def shop_weapons(callback: types.CallbackQuery):
    logging.info(f'User {callback.message.from_user.id}/{callback.message.from_user.full_name} shopping weapons')
    await callback.message.delete()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Дубинка 1 \U0001fa99', callback_data='buy_brass_knuckles'),
            InlineKeyboardButton(text='Кинжал 2 \U0001fa99', callback_data='buy_knife')
        ],
        [
            InlineKeyboardButton(text='Меч 3 \U0001fa99', callback_data='buy_sword'),
            InlineKeyboardButton(text='Назад \U0001f6aa', callback_data='back_to_shop')
        ]
    ])
    
    await callback.message.answer("Выберите оружие:", reply_markup=keyboard)

@dp.callback_query(F.data == 'shop_armor')
async def shop_armor(callback: types.CallbackQuery):
    logging.info(f'User {callback.message.from_user.id}/{callback.message.from_user.full_name} shopping armor')
    await callback.message.delete()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Кожанный доспех 1 \U0001fa99', callback_data='buy_leather_armor'),
            InlineKeyboardButton(text='Кольчуга 2 \U0001fa99', callback_data='buy_chain_armor')
        ],
        [
            InlineKeyboardButton(text='Латный доспех 3 \U0001fa99', callback_data='buy_heavy_armor'),
            InlineKeyboardButton(text='Назад \U0001f6aa', callback_data='back_to_shop')
        ]
    ])
    
    await callback.message.answer("Все просто - больше денег = больше защиты, естественно в ущерб подвижности. \nВыберите броню:", reply_markup=keyboard)

@dp.callback_query(F.data == 'shop_potions')
async def shop_potions(callback: types.CallbackQuery):
    logging.info(f'User {callback.message.from_user.id}/{callback.message.from_user.full_name} shopping potions')
    await callback.message.delete()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Малое зелье лечения 1 \U0001fa99', callback_data='buy_small_health_potion'),
            InlineKeyboardButton(text='Среднее зелье лечения 2 \U0001fa99', callback_data='buy_medium_health_potion')
        ],
        [
            InlineKeyboardButton(text='Большое зелье лечения 3 \U0001fa99', callback_data='buy_large_health_potion'),
            InlineKeyboardButton(text='Зелье маны 2 \U0001fa99', callback_data='buy_mana_potion')
        ],
        [
            InlineKeyboardButton(text='Зелье силы 4 \U0001fa99', callback_data='buy_strength_potion'),
            InlineKeyboardButton(text='Назад \U0001f6aa', callback_data='back_to_shop')
        ]
    ])
    
    await callback.message.answer("На столе стоит табличка 'Зелье маны необходимо только волшебникам, покупайте с умом !'\nВыберите зелье:", reply_markup=keyboard)

# Обработчик для покупки предметов

# Обработчик для возврата в магазин
@dp.callback_query(F.data == 'back_to_shop')
async def back_to_shop(callback: types.CallbackQuery):
    logging.info(f'User {callback.message.from_user.id}/{callback.message.from_user.full_name} go back to shop')
    character = get_character(callback.from_user.id)
    # Удаляем предыдущее сообщение с магазином
    await callback.message.delete()
    await asyncio.sleep(1)
    # Отправляем новое сообщение с информацией о деньгах
    await callback.message.answer(text=f'Сейчас у вас {character.money} монет', reply_markup=await start_shop(callback.message))


@dp.callback_query(F.data == 'buy_krekers')
async def buy_krekers(callback: types.CallbackQuery):
    character = get_character(callback.from_user.id)
    if character is None:
        await callback.answer("Сначала начните игру, чтобы получить персонажа!")
        return

    if character.money < 1:  # Предположим, что сухари стоят 1 монету
        await callback.answer("У вас недостаточно денег!")
        return

    character.inventory.add_item(krekers, character)  # Добавляем предмет в инвентарь
    character.money -= 1  # Уменьшаем количество денег
    await callback.message.delete()
    await asyncio.sleep(2)
    await callback.message.answer(f"Вы купили Сухари! \U0001f968\nУ вас осталось {character.money} монет.", reply_markup=callback.message.reply_markup)

@dp.callback_query(F.data == 'buy_bread')
async def buy_bread(callback: types.CallbackQuery):
    character = get_character(callback.from_user.id)
    if character is None:
        await callback.answer("Сначала начните игру, чтобы получить персонажа!")
        return

    if character.money < 2:  # Предположим, что хлеб стоит 2 монеты
        await callback.answer("У вас недостаточно денег!")
        return

    character.inventory.add_item(bread, character)  # Добавляем хлеб в инвентарь
    character.money -= 2  # Уменьшаем количество денег
    await callback.message.delete()
    await asyncio.sleep(2)
    await callback.message.answer(f"Вы купили Хлеб! \U0001f35e\nУ вас осталось {character.money} монет.", reply_markup=callback.message.reply_markup)

@dp.callback_query(F.data == 'buy_meat')
async def buy_meat(callback: types.CallbackQuery):
    character = get_character(callback.from_user.id)
    if character is None:
        await callback.answer("Сначала начните игру, чтобы получить персонажа!")
        return

    if character.money < 3:  # Предположим, что мясо стоит 3 монеты
        await callback.answer("У вас недостаточно денег!")
        return

    character.inventory.add_item(meat, character)  # Добавляем мясо в инвентарь
    character.money -= 3  # Уменьшаем количество денег
    await callback.message.delete()
    await asyncio.sleep(2)
    await callback.message.answer(f"Вы купили Мясо! \U0001f356\nУ вас осталось {character.money} монет.", reply_markup=callback.message.reply_markup)

@dp.callback_query(F.data == 'buy_brass_knuckles')
async def buy_brass_knuckles(callback: types.CallbackQuery):
    character = get_character(callback.from_user.id)
    if character is None:
        await callback.answer("Сначала начните игру, чтобы получить персонажа!")
        return

    if character.money < 1:  # Предположим, что кастеты стоят 5 монет
        await callback.answer("У вас недостаточно денег!")
        return

    character.inventory.add_item(brass_knuckles, character)  # Добавляем кастеты в инвентарь
    character.money -= 1  # Уменьшаем количество денег
    await callback.message.delete()
    await asyncio.sleep(2)
    await callback.message.answer(f"Вы купили дубинку! \U0001f528\nУ вас осталось {character.money} монет.", reply_markup=callback.message.reply_markup)

@dp.callback_query(F.data == 'buy_knife')
async def buy_knife(callback: types.CallbackQuery):
    character = get_character(callback.from_user.id)
    if character is None:
        await callback.answer("Сначала начните игру, чтобы получить персонажа!")
        return

    if character.money < 2:  # Предположим, что кинжал стоит 4 монеты
        await callback.answer("У вас недостаточно денег!")
        return

    character.inventory.add_item(knife, character)  # Добавляем кинжал в инвентарь
    character.money -= 2  # Уменьшаем количество денег
    await callback.message.delete()
    await asyncio.sleep(2)
    await callback.message.answer(f"Вы купили Кинжал! \U0001f5e1\uFE0F\nУ вас осталось {character.money} монет.", reply_markup=callback.message.reply_markup)

@dp.callback_query(F.data == 'buy_sword')
async def buy_sword(callback: types.CallbackQuery):
    character = get_character(callback.from_user.id)
    if character is None:
        await callback.answer("Сначала начните игру, чтобы получить персонажа!")
        return

    if character.money < 3:  # Предположим, что меч стоит 6 монет
        await callback.answer("У вас недостаточно денег!")
        return

    character.inventory.add_item(sword, character)  # Добавляем меч в инвентарь
    character.money -= 3  # Уменьшаем количество денег
    await callback.message.delete()
    await asyncio.sleep(2)
    await callback.message.answer(f"Вы купили Меч! \u2694\uFE0F\nУ вас осталось {character.money} монет.", reply_markup=callback.message.reply_markup)

@dp.callback_query(F.data == 'buy_leather_armor')
async def buy_leather_armor(callback: types.CallbackQuery):
    character = get_character(callback.from_user.id)
    if character is None:
        await callback.answer("Сначала начните игру, чтобы получить персонажа!")
        return

    if character.money < 1:  # Предположим, что кожанный доспех стоит 7 монет
        await callback.answer("У вас недостаточно денег!")
        return

    character.inventory.add_item(leather_armor, character)  # Добавляем кожанный доспех в инвентарь
    character.money -= 1  # Уменьшаем количество денег
    character.agility -= 10
    await callback.message.delete()
    await asyncio.sleep(2)
    await callback.message.answer(f"Вы купили Кожанный доспех! \U0001f6e1\uFE0F\nУ вас осталось {character.money} монет.", reply_markup=callback.message.reply_markup)

@dp.callback_query(F.data == 'buy_chain_armor')
async def buy_chain_armor(callback: types.CallbackQuery):
    character = get_character(callback.from_user.id)
    if character is None:
        await callback.answer("Сначала начните игру, чтобы получить персонажа!")
        return

    if character.money < 2:  # Предположим, что кольчуга стоит 10 монет
        await callback.answer("У вас недостаточно денег!")
        return

    character.inventory.add_item(chain_armor, character)  # Добавляем кольчугу в инвентарь
    character.money -= 2  # Уменьшаем количество денег
    character.agility -= 20
    await callback.message.delete()
    await asyncio.sleep(2)
    await callback.message.answer(f"Вы купили Кольчугу! \U0001f6e1\uFE0F\nУ вас осталось {character.money} монет.", reply_markup=callback.message.reply_markup)

@dp.callback_query(F.data == 'buy_heavy_armor')
async def buy_heavy_armor(callback: types.CallbackQuery):
    character = get_character(callback.from_user.id)
    if character is None:
        await callback.answer("Сначала начните игру, чтобы получить персонажа!")
        return

    if character.money < 3:  # Предположим, что латный доспех стоит 12 монет
        await callback.answer("У вас недостаточно денег!")
        return

    character.inventory.add_item(heavy_armor, character)
    character.money -= 3  # Уменьшаем количество денег
    character.agility -= 30
    await callback.message.delete()
    await asyncio.sleep(2)
    await callback.message.answer(f"Вы купили Латный доспех! \U0001f6e1\uFE0F\nУ вас осталось {character.money} монет.", reply_markup=callback.message.reply_markup)

@dp.callback_query(F.data == 'buy_small_health_potion')
async def buy_small_health_potion(callback: types.CallbackQuery):
    character = get_character(callback.from_user.id)
    if character is None:
        await callback.answer("Сначала начните игру, чтобы получить персонажа!")
        return

    if character.money < 1:  # Предположим, что малое зелье лечения стоит 1 монету
        await callback.answer("У вас недостаточно денег!")
        return

    character.inventory.add_item(small_health_potion, character)  # Добавляем малое зелье лечения в инвентарь
    character.money -= 1  # Уменьшаем количество денег
    await callback.message.delete()
    await asyncio.sleep(2)
    await callback.message.answer(f"Вы купили Малое зелье лечения! \U0001f9ea\nУ вас осталось {character.money} монет.", reply_markup=callback.message.reply_markup)

@dp.callback_query(F.data == 'buy_medium_health_potion')
async def buy_medium_health_potion(callback: types.CallbackQuery):
    character = get_character(callback.from_user.id)
    if character is None:
        await callback.answer("Сначала начните игру, чтобы получить персонажа!")
        return

    if character.money < 2:  # Предположим, что среднее зелье лечения стоит 3 монеты
        await callback.answer("У вас недостаточно денег!")
        return

    character.inventory.add_item(medium_health_potion, character)  # Добавляем среднее зелье лечения в инвентарь
    character.money -= 2  # Уменьшаем количество денег
    await callback.message.delete()
    await asyncio.sleep(2)
    await callback.message.answer(f"Вы купили Среднее зелье лечения! \U0001f9ea\nУ вас осталось {character.money} монет.", reply_markup=callback.message.reply_markup)

@dp.callback_query(F.data == 'buy_large_health_potion')
async def buy_large_health_potion(callback: types.CallbackQuery):
    character = get_character(callback.from_user.id)
    if character is None:
        await callback.answer("Сначала начните игру, чтобы получить персонажа!")
        return

    if character.money < 3:  # Предположим, что большое зелье лечения стоит 5 монет
        await callback.answer("У вас недостаточно денег!")
        return

    character.inventory.add_item(large_health_potion, character)  # Добавляем большое зелье лечения в инвентарь
    character.money -= 3  # Уменьшаем количество денег
    await callback.message.delete()
    await asyncio.sleep(2)
    await callback.message.answer(f"Вы купили Большое зелье лечения! \U0001f9ea\nУ вас осталось {character.money} монет.", reply_markup=callback.message.reply_markup)

@dp.callback_query(F.data == 'buy_mana_potion')
async def buy_mana_potion(callback: types.CallbackQuery):
    character = get_character(callback.from_user.id)
    if character is None:
        await callback.answer("Сначала начните игру, чтобы получить персонажа!")
        return

    if character.money < 2:  # Предположим, что зелье маны стоит 4 монеты
        await callback.answer("У вас недостаточно денег!")
        return

    character.inventory.add_item(mana_potion, character)  # Добавляем зелье маны в инвентарь
    character.money -= 2  # Уменьшаем количество денег
    await callback.message.delete()
    await asyncio.sleep(2)
    await callback.message.answer(f"Вы купили Зелье маны! \u2697\uFE0F\nУ вас осталось {character.money} монет.", reply_markup=callback.message.reply_markup)

@dp.callback_query(F.data == 'buy_strength_potion')
async def buy_strength_potion(callback: types.CallbackQuery):
    character = get_character(callback.from_user.id)
    if character is None:
        await callback.answer("Сначала начните игру, чтобы получить персонажа!")
        return

    if character.money < 4:  # Предположим, что зелье силы стоит 2 монеты
        await callback.answer("У вас недостаточно денег!")
        return

    character.inventory.add_item(strength_potion, character)  # Добавляем зелье силы в инвентарь
    character.money -= 4  # Уменьшаем количество денег
    await callback.message.delete()
    await asyncio.sleep(2)
    await callback.message.answer(f"Вы купили Зелье силы! \U0001f4aa\nУ вас осталось {character.money} монет.", reply_markup=callback.message.reply_markup)

current_level_index = 0
enemys = []
loot = []
current_target = None  # Инициализируем переменную
random_loot = None
descript = None
photo = None

def update_enemies():
    global enemys
    if current_level_index < len(levels):
        enemys = levels[current_level_index].enemies.copy() if levels[current_level_index].enemies else []
    else:
        enemys = []

def update_loot():
    global loot
    if current_level_index < len(levels):
        loot = levels[current_level_index].loot.copy() if levels[current_level_index].loot else []
    else:
        loot = []

def update_descript():
    global descript
    if current_level_index < len(levels):
        descript = levels[current_level_index].descript if levels[current_level_index].descript else []
    else:
        descript = None

def update_photo():
    global photo
    if current_level_index < len(levels):
        photo = levels[current_level_index].photo if levels[current_level_index].photo else []
    else:
        photo = []
        # with open(photo, 'rb') as photo:

def main_loop(player):
    player.loot = levels[player.current_level_index].loot.copy() if levels[player.current_level_index].loot else []
    player.enemies = levels[player.current_level_index].enemies.copy() if levels[player.current_level_index].enemies else []
    player.descript = levels[player.current_level_index].descript if levels[player.current_level_index].descript else None
    player.photo = levels[player.current_level_index].photo if levels[player.current_level_index].photo else None

    # Сбрасываем флаг исследования
    player.has_researched = False
    
    # Сброс здоровья врагов
    for enemy in player.enemies:
        enemy.reset_health()

    if player.loot:
        player.random_loot = random.choice(player.loot)
    else:
        player.random_loot = None

    if player.enemies:
        player.current_target = random.choice(player.enemies)
    else:
        player.current_target = None

@dp.callback_query(F.data == 'start_adventure')
async def start_adventure(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    character = get_character(user_id)

    if character is None:
        await callback.answer("Сначала начните игру, чтобы получить персонажа!")
        return

    await callback.message.answer(f'Вы направляетесь к новым свершениям, у вас \n{character.inventory.show_inventory()} \nВ вашем кошельке{character.money} монет.', parse_mode='HTML')
    photo = FSInputFile(photo_2)  

    await bot.send_photo(chat_id=callback.message.chat.id, photo=photo, caption='Тихие пролески сменяются полями, реками и озерами, после полудня пути вы входите на земли Пепельных равнин. \nЭти земли некогда славились своей красотой, но чем ближе вы к замку Каструм Нахт, тем больше кажется что вы из жаркого лета переместились в позднюю осень.')
                                  
    await asyncio.sleep(2)
    photo = FSInputFile(photo_3)  
    Player.reset_game(character)
    
    await bot.send_photo(chat_id=callback.message.chat.id, photo=photo, caption='Вот вы уже на обширном кладбище этих земель, еще чуть чуть и вы попадете в прилегающую к замку деревню. \nВы видите несколько сомнительных личностей, роющихся у ближайших могил. Когда вы приближаетесь они со злобой смотрят на вас и начинают приближаться...в руке одного из них блеснул нож')
    await asyncio.sleep(2)

    player = get_player(user_id)
    player.current_level_index = 0
    main_loop(player)
    action_kb = await play_kb(user_id)
    await callback.message.answer("Что вы хотите сделать?", reply_markup=action_kb)

# Добавляем переменную для отслеживания состояния атаки
is_ready_to_attack = False

@dp.message(F.text == 'Приготовиться к бою \u2694\uFE0F')
async def attack_enemy(message: types.Message):
    global current_target, current_level_index, random_loot, descript, photo, player, is_ready_to_attack

    user_id = message.from_user.id
    character = get_character(user_id)
    player = get_player(user_id)

    if character is None:
        await message.answer('Сначала начните игру, чтобы получить персонажа!\n/start')
        return

    # Получаем текущих врагов
    enemies = player.enemies  # Используем врагов из игрока  
    if not enemies:
        await message.answer("Нет доступных врагов для атаки.")
        return

    # Формируем список врагов
    enemy_list = "\n".join([f"{i + 1}. {enemy.name} (HP: {enemy.hp})" for i, enemy in enumerate(enemies)])
    await message.answer(f'Возможный урон от результата броска кости:\n1. От 1 до {character.strength//5}\n2. От 5 до {character.strength//4}\n3. От 5 до {character.strength//2}\n4. От 5 до {character.strength}\n5. От 20 до {character.strength}6. От 20 до {character.strength*2}\n\nВаши враги:\n{enemy_list}\nВыберите номер врага, которого хотите атаковать:')

    # Устанавливаем состояние готовности к атаке
    is_ready_to_attack = True

@dp.message(lambda message: message.text.isdigit())
async def choose_enemy(message: types.Message):
    global current_target, current_level_index, random_loot, descript, photo, is_ready_to_attack

    user_id = message.from_user.id
    character = get_character(user_id)
    player = get_player(user_id)

    if character is None:
        await message.answer('Сначала начните игру, чтобы получить персонажа !')
        return

    if not is_ready_to_attack:
        await message.answer("Сначала нужно приготовиться к бою !")
        return

    enemy_index = int(message.text) - 1  # Преобразуем текст в индекс

    if 0 <= enemy_index < len(player.enemies):
        current_target = player.enemies[enemy_index]  # Устанавливаем текущую цель
        await message.answer(f'Вы выбрали {current_target.name} в качестве цели!')
        # Удаляем предыдущее сообщение
        await asyncio.sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        
        # Теперь можно продолжить логику атаки
        await perform_attack(message)
    else:
        await message.answer("Неверный номер. Пожалуйста, выберите номер из списка.")

async def perform_attack(message: types.Message):
    global current_target, current_level_index, random_loot, descript, photo, is_ready_to_attack
    # Удаляем предыдущее сообщение
    await asyncio.sleep(2)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    
    user_id = message.from_user.id
    character = get_character(user_id)
    # Логика атаки
    attack_roll = await message.answer_dice("\U0001f3b2")
    attack = attack_roll.dice.value
    await asyncio.sleep(4)
    if attack <= current_target.armor:
        await message.answer(f"Ваша атака не пробила броню {current_target.name}")
        enemy_damage = random.randint(10, current_target.strength)  # Урон врага равен его силе
        character.hp -= enemy_damage  # Уменьшаем здоровье персонажа
        await message.answer(f'{current_target.name} атакует в ответ {character.name} и наносит {enemy_damage} урона!')
        if character.hp <= 0:
            await message.answer(f'{character.name} был повержен в бою!')
            Player.reset_game(character)
            player.current_level_index = 0
            main_loop(player)
            await message.reply('Вы погибли, попробуйте еще',
                reply_markup= await main_kb(message.from_user.id))
                        
        else:
            await message.answer(f'{character.name} осталось {character.hp} здоровья.')
            return None

    if current_target.dodge():
        await message.answer(f'{current_target.name} уклоняется от атаки {character.name}!')
        enemy_damage = random.randint(10, current_target.strength)  # Урон врага равен его силе
        character.hp -= enemy_damage  # Уменьшаем здоровье персонажа
        await message.answer(f'{current_target.name} атакует в ответ {character.name} и наносит {enemy_damage} урона!')
        if character.hp <= 0:
            await message.answer(f'{character.name} был повержен в бою!')
            Player.reset_game(character)
            player.current_level_index = 0
            main_loop(player)
            await message.reply('Вы погибли, попробуйте еще',
                reply_markup= await main_kb(message.from_user.id))
            
                        
        else:
            await message.answer(f'{character.name} осталось {character.hp} здоровья.')
            return None

        # Удаляем сообщение о неудачной атаке
        await asyncio.sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)  

    else:
        if attack == 1:
            damage = random.randint(1, character.strength//5)
        elif attack == 2:
            damage = random.randint(5, character.strength//4)
        elif attack == 3:
            damage = random.randint(5, character.strength//2)
        elif attack == 4:
            damage = random.randint(5, character.strength)
        elif attack == 5:
            damage = random.randint(20, character.strength)
        elif attack == 6:
            damage = random.randint(20, character.strength*2)

        current_target.hp -= damage
        await message.answer(f'{character.name} атакует {current_target.name} и наносит {damage} урона!')

        if current_target.hp <= 0:
            await message.answer(f'{current_target.name} повержен!')
            player.enemies.remove(current_target)  # Удаляем поверженного бандита
            current_target = None  # Сбрасываем цель
        else:
            await message.answer(f'{current_target.name} осталось {current_target.hp} здоровья.')

            # Враг атакует в ответ
            if character.dodge():
                await message.answer(f'{character.name} ловко уклонился от атаки {current_target.name}')
            else:
                # Враг колдует
                if current_target.tipe == 'wither':
                    cast = await message.answer_dice("\U0001f3b2")
                    cast_value = cast.dice.value
                    if cast_value > 2:
                        await asyncio.sleep(4)
                        enemy_spels = [darkness_bolt, hunger_damage]
                        spell = random.choice(enemy_spels)
                        enemy_result_message = Magic.cast_spell(current_target, spell, character)
                        await message.answer(enemy_result_message)
                    else:
                        await asyncio.sleep(4)
                        await message.answer("Врагу не удается применить заклинание и он ошеломлен !")
                        return None
                elif current_target.tipe == 'вампир':
                    enemy_spels = [darkness_bolt, hunger_damage, vampirism]
                    spell = random.choice(enemy_spels)
                    enemy_result_message = Magic.cast_spell(current_target, spell, character)
                    await message.answer(enemy_result_message)

                rod = await message.answer_dice("\U0001f3b2")
                await asyncio.sleep(4)
                dice_value = rod.dice.value
                if dice_value > character.armor:
                    enemy_damage = random.randint(1, current_target.strength) # Урон врага равен его силе
                    character.hp -= enemy_damage  # Уменьшаем здоровье персонажа
                    await message.answer(f'{current_target.name} атакует {character.name} и наносит {enemy_damage} урона!')
                    if character.hunger <= 0:
                        await message.answer(f'{character.name} умер от голода!')
                        Player.reset_game(character)
                        player.current_level_index = 0
                        main_loop(player)
                        await message.reply('НУ а как ты хотел ? Доставку еды еще не изобрели',
                                        reply_markup= await main_kb(message.from_user.id))
                        
                    if character.hp <= 0:
                        await message.answer(f'{character.name} был повержен в бою!')
                        Player.reset_game(character)
                        player.current_level_index = 0
                        main_loop(player)
                        await message.reply('Вы погибли, попробуйте еще',
                                reply_markup= await main_kb(message.from_user.id))
                        
                    else:
                        await message.answer(f'{character.name} осталось {character.hp} здоровья.')
                else:
                    await message.answer(f'Атака {current_target.name} не пробила броню {character.name}!')
    # После завершения атаки сбрасываем состояние
    is_ready_to_attack = False
    # Проверка, остались ли бандиты
    if not player.enemies:
        
        random_loots = player.loot
        random_loot = random.choice(random_loots)
        character.inventory.add_item(random_loot, character)
        await asyncio.sleep(1)
        await message.answer(f'Голод:{character.hunger} - 1 \nУ вас осталось {character.hunger - 1} сытости')
        character.hunger -= 1
        await asyncio.sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await message.answer(f'Все враги повержены! Вы победили!\nПосле победы над врагами вы находите:\n{random_loot}', parse_mode = "HTML")
        photo = FSInputFile(player.photo)
        await asyncio.sleep(1)

        await asyncio.sleep(1)
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=levels[player.current_level_index].descript)
        #await message.answer(descript)
        current_target = None  # Сбрасываем цель после победы
        if player.current_level_index == 4:
            mess = river_port(character)
            await message.answer(mess)
            if character.hp <= 0:
                await message.answer(f'{character.name} утонул')
                Player.reset_game(character)
                player.current_level_index = 0
                main_loop(player)
                await message.reply('Добро пожаловать !',
                         reply_markup= await main_kb(message.from_user.id))
                
        elif player.current_level_index == 7:
            await message.answer("Вы победили, теперь, когда угроза миновала вы чувствуете как сильно устали. Вы идете обратно, забрав артефакт, который служил вампиру")
            Player.reset_game(character) # Сбрасываем уровень на стартовый
            player.current_level_index = 0
            main_loop(player)
            await message.reply('Добро пожаловать, снова',
                            reply_markup= await main_kb(message.from_user.id))
            return None
    # Проверяем, не упал ли голод до нуля
        if character.hunger <= 0:
            await asyncio.sleep(1)
            await message.answer(f'{character.name} умер от голода!')
            Player.reset_game(character)
            player.current_level_index = 0
            main_loop(player)
            await message.reply('НУ а как ты хотел ? Доставку еды еще не изобрели',
                            reply_markup= await main_kb(message.from_user.id))
            
        player.current_level_index += 1
        main_loop(player)

@dp.message(F.text == 'Скрыться \U0001f464')
async def hide_from_enemy(message: types.Message):
    global current_level_index, random_loot, descript, photo
    user_id = message.from_user.id
    character = get_character(user_id)
    player = get_player(user_id)

    if character is None:
        await message.answer("Сначала начните игру, чтобы получить персонажа!")
        return

    global current_target
    enemies = player.enemies  # Используем врагов из игрока  
    if not enemies:
        await message.answer("Нет доступных врагов для атаки.")

    # Если цель еще не выбрана, выбираем ее
    if current_target is None:
        current_target = random.choice(enemies)  # Выбираем случайного врага
        await message.answer(f'Вы пытаетесь скрыться от {current_target.name}')

    # Логика для скрытия
    stealth_success = character.agility > current_target.perception

    if stealth_success:
        await message.answer(f"{character.name} успешно скрывается от {current_target.name}!")
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await asyncio.sleep(1)
        await message.answer(f'Голод:{character.hunger} - 1 осталось {character.hunger - 1}')
        character.hunger -= 1
        photo = FSInputFile(player.photo) 
        current_target = None
        await asyncio.sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=levels[player.current_level_index].descript)
        if character.hunger <= 0:
            await asyncio.sleep(1)
            await message.answer(f'{character.name} умер от голода!')
            Player.reset_game(character)
            player.current_level_index = 0
            main_loop(player)
            await message.reply('НУ а как ты хотел ? Доставку еды еще не изобрели',
                            reply_markup= await main_kb(message.from_user.id))
        if current_level_index == 4:
            mess = river_port(character)
            await message.answer(mess)
            if character.hp <= 0:
                await asyncio.sleep(1)
                await message.answer(f'{character.name} утонул')
                Player.reset_game(character)
                player.current_level_index = 0
                main_loop(player)
                await message.reply('Добро пожаловать !',
                         reply_markup= await main_kb(message.from_user.id))
                
        elif current_level_index == 7:
            await message.answer("Вы победили, теперь, когда угроза миновала вы чувствуете как сильно устали. Вы идете обратно, забрав артефакт, который служил вампиру")
            Player.reset_game(character) # Сбрасываем уровень на стартовый
            player.current_level_index = 0
            main_loop(player)
            await message.reply('Добро пожаловать, снова',
                            reply_markup= await main_kb(message.from_user.id))
        
        player.current_level_index += 1
        main_loop(player)
    else:
        await message.answer(f"{character.name} не смог скрыться и столкнулся с {current_target.name}!")
        await asyncio.sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

        enemy_damage = current_target.strength
        character.hp -= enemy_damage
        await message.answer(f"{current_target.name} атакует {character.name} и наносит {enemy_damage} урона!\nУ вас осталось {character.hp} здоровья")
        await asyncio.sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

        if character.hp <= 0:
            await message.answer(f'{character.name} был повержен в бою!')
            Player.reset_game(character)
            player.current_level_index = 0
            main_loop(player)
            await message.reply('Добро пожаловать !',
                        reply_markup= await main_kb(message.from_user.id))
            

        await message.answer(f"{character.name} осталось {character.hp} здоровья.")

    # Проверка, остались ли бандиты
    if not player.enemies:
        random_loots = player.loot
        random_loot = random.choice(random_loots)
        character.inventory.add_item(random_loot, character)
        await message.answer(f'Все враги повержены! Вы победили!\nПосле победы над врагами вы находите:\n{random_loot}', parse_mode = "HTML")
        photo = FSInputFile(player.photo)
        await asyncio.sleep(1)

        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=levels[player.current_level_index].descript)
        #await message.answer(descript)
        await message.answer(f'Голод:{character.hunger} - 1 осталось {character.hunger - 1}')
        character.hunger -= 1
        current_target = None  # Сбрасываем цель после победы
        if player.current_level_index == 4:
            mess = river_port(character)
            await message.answer(mess)
            if character.hp <= 0:
                await message.answer(f'{character.name} утонул')
                Player.reset_game(character)
                player.current_level_index = 0
                main_loop(player)
                await message.reply('Добро пожаловать !',
                         reply_markup= await main_kb(message.from_user.id))
                
        elif player.current_level_index == 7:
            await message.answer("Вы победили, теперь, когда угроза миновала вы чувствуете как сильно устали. Вы идете обратно, забрав артефакт, который служил вампиру")
            Player.reset_game(character) # Сбрасываем уровень на стартовый
            player.current_level_index = 0
            main_loop(player)
            await message.reply('Добро пожаловать, снова',
                            reply_markup= await main_kb(message.from_user.id))
            
    # Проверяем, не упал ли голод до нуля
        if character.hunger <= 0:
            await asyncio.sleep(1)
            await message.answer(f'{character.name} умер от голода!')
            Player.reset_game(character)
            player.current_level_index = 0
            main_loop(player)
            await message.reply('НУ а как ты хотел ? Доставку еды еще не изобрели',
                            reply_markup= await main_kb(message.from_user.id))
            
        player.current_level_index += 1
        main_loop(player)

# Определение состояний
class Form(StatesGroup):
    waiting_for_response = State()

# Обработчик для показа инвентаря
@dp.message(F.text == 'Инвентарь \U0001f392')
async def show_inventory(message: types.Message):
    user_id = message.from_user.id
    character = get_character(user_id)
    # item = message.text
    
    if character is None:
        await message.answer("Сначала начните игру, чтобы получить персонажа!")
        return

    inventory = character.inventory.show_inventory()
    if inventory == "Инвентарь пуст.":
        await message.answer(inventory)
        return

    await message.answer(f'{character.character_info()}\n\nВаш инвентарь:\n{inventory} \n\nЧтобы использовать предмет, скопируйте и вставьте его название.', parse_mode='HTML')
    
    @dp.message(lambda message: True)
    async def answer_item(message: types.Message, state: FSMContext):
        user_id = message.from_user.id
        character = get_character(user_id)
        item_name = message.text
        
        result_message = character.inventory.use_item(item_name, character)
        await message.answer(result_message)

@dp.message(F.text == 'Изучить место \U0001f4dc')
async def handle_defend(message: types.Message):
    global current_level_index
    user_id = message.from_user.id
    character = get_character(user_id)
    player = players.get(user_id)

    if player is None:
        await message.answer('Сначала начните игру, чтобы получить персонажа!')
        return

    if player.has_researched:
        await message.answer("Вы уже исследовали это место.")
        return  # Добавьте return, чтобы не продолжать выполнение кода

    player.has_researched = True  # Устанавливаем флаг исследования

    # Логика нахождения предмета
    secret_loot = [krekers, fish, krekers, krekers, bread, meat, meat, apple, cheese, fish, berry, root_meat, root_meat, root_meat, run_of_destroy, boots, shield]
    found_item = random.choice(secret_loot)
    character.inventory.add_item(found_item, character)
    character.hunger -= 1
    if character.hunger <= 0:
        await message.answer(f'{character.name} умер от голода!')
        Player.reset_game(character)
        current_level_index = 0
        main_loop()
        await message.reply('НУ а как ты хотел ? Доставку еды еще не изобрели',
                            reply_markup= await main_kb(message.from_user.id))
    else:
        await asyncio.sleep(1)
        await message.answer(f'Вы изучили место и нашли: {found_item.name}! \nВаш уровень голода снизился на 1. Текущий уровень голода: {character.hunger}.')

@dp.message(F.text == 'Особые умения \U0001f31f')
async def magic_menu(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Огненный шар \U0001f525', callback_data='fireball'),
            InlineKeyboardButton(text='Щит света \U0001f315', callback_data='cristal_shield')
        ],
        [
            InlineKeyboardButton(text='Цепная молния \u26A1', callback_data='shock'),
            InlineKeyboardButton(text='Метеор \U0001f320', callback_data='meteor')
        ],
        [
            InlineKeyboardButton(text='Исцеление \u2764\uFE0F', callback_data='heall')
        ]
    ])

    await message.answer(
        "Выберите заклинание",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data in ['fireball', 'cristal_shield', 'shock', 'meteor', 'heall'])
async def handle_spell_cast(callback: types.CallbackQuery):
    global current_target, current_level_index, random_loot, descript, photo  # Используем глобальную переменную для текущей цели
    user_id = callback.from_user.id
    character = get_character(user_id)
    player = get_player(user_id)

    if character is None:
        await callback.answer('Сначала начните игру, чтобы получить персонажа!')
        return

    # Проверка имени персонажа
    if character.name != "Моргана":
        await callback.message.answer('Вы не умеете колдовать !') 
        return
    
    # Получаем врагов
    global enemys  # Убедимся, что мы используем глобальный список врагов
    if not player.enemies:
        await callback.answer('Нет доступных врагов для атаки!')
        return

    # Если цель еще не выбрана, выбираем ее
    if current_target is None:
        current_target = random.choice(player.enemies)  # Выбираем случайного врага

    # Переменная для хранения сообщения о результате
    result_message = ""

    if callback.data == 'fireball':
        await callback.message.answer('\U0001f525')
        spell = fireball
        result_message = Magic.cast_spell(character, spell, current_target)  # Применение заклинания огненного шара
        if current_target.hp <= 0:
            result_message += f"{current_target.name} повержен!\n"
            player.enemies.remove(current_target)  # Удаляем поверженного врага
            current_target = None  # Сбрасываем цель
    elif callback.data == 'cristal_shield':
        await callback.message.answer('\u2600\uFE0F')
        spell = armor
        result_message = Magic.cast_spell(character, spell)  # Применение заклинания на себя
    elif callback.data == 'shock':
        await callback.message.answer('\u26A1')
        spell = shock
        for current_target in player.enemies:
            result_message += Magic.cast_spell(character, spell, current_target) + '\n'  # Применение цепной молнии
            if current_target.hp <= 0:
                result_message += f"{current_target.name} повержен!\n"
                player.enemies.remove(current_target) # Удаляем поверженного врага
        current_target = None  # Сбрасываем цель после применения заклинания
    elif callback.data == 'meteor':
        await callback.message.answer('\U0001f4ab')
        spell = meteor
        for current_target in player.enemies:
            result_message += Magic.cast_spell(character, spell, current_target) + '\n'  # Применение метеоритного дождя
            if current_target.hp <= 0:
                result_message += f"{current_target.name} повержен!\n"
                player.enemies.remove(current_target)  # Удаляем поверженного бандита
        current_target = None  # Сбрасываем цель после применения заклинания
    elif callback.data == 'heall':
        await callback.message.answer('\u2764\uFE0F')
        spell = heal
        result_message = Magic.cast_spell(character, spell)

    # Отправляем результат пользователю
    await callback.message.answer(result_message)

    # Проверка, остались ли враги
    if not player.enemies:
        random_loots = player.loot
        random_loot = random.choice(random_loots)
        character.inventory.add_item(random_loot, character)
        await callback.message.answer(f'Все враги повержены! Вы победили!\nПосле победы над врагами вы находите с их тел\n{random_loot}', parse_mode = "HTML")
        await callback.message.answer(f'Голод:{character.hunger} - 1 осталось {character.hunger - 1}')
        character.hunger -= 1
        photo = FSInputFile(player.photo)  

        await bot.send_photo(chat_id=callback.message.chat.id, photo=photo, caption=levels[player.current_level_index].descript)
        #await message.answer(descript)
        current_target = None  # Сбрасываем цель после победы
        if current_level_index == 4:
            mess = river_port(character)
            await callback.message.answer(mess)
            if character.hp <= 0:
                await asyncio.sleep(1)
                await callback.message.answer(f'{character.name} тонет')
                Player.reset_game(character)
                player.current_level_index = 0
                main_loop(player)
                await callback.message.reply('Добро пожаловать !',
                         reply_markup= await main_kb(callback.message.from_user.id))
                
        elif current_level_index == 7:
            await callback.message.answer("Вы победили, теперь, когда угроза миновала вы чувствуете как сильно устали. Вы идете обратно, забрав артефакт, который служил вампиру")
            Player.reset_game(character) # Сбрасываем уровень на стартовый
            player.current_level_index = 0
            main_loop(player)
            await callback.message.reply('Добро пожаловать, снова',
                            reply_markup= await main_kb(callback.message.from_user.id))
            
    # Проверяем, не упал ли голод до нуля
        if character.hunger <= 0:
            await asyncio.sleep(1)
            await callback.message.answer(f'{character.name} умер от голода!')
            Player.reset_game(character)
            player.current_level_index = 0
            main_loop(player)
            await callback.message.reply('НУ а как ты хотел ? Доставку еды еще не изобрели',
                            reply_markup= await main_kb(callback.message.from_user.id))
            
        player.current_level_index += 1
        main_loop(player)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
