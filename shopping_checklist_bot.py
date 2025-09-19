import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# В памяти, для одного пользователя
shopping_lists = {}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот-чеклист для покупок.\n"
                        "Добавь товар: /add хлеб\n"
                        "Показать список: /list\n"
                        "Удалить: /remove хлеб\n"
                        "Отметить купленным: /done хлеб")

@dp.message_handler(commands=['add'])
async def add_item(message: types.Message):
    user_id = message.from_user.id
    item = message.get_args()
    if not item:
        await message.reply("Что добавить? Используй: /add товар")
        return
    shopping_lists.setdefault(user_id, set()).add(item)
    await message.reply(f"Добавлено: {item}")

@dp.message_handler(commands=['list'])
async def show_list(message: types.Message):
    user_id = message.from_user.id
    items = shopping_lists.get(user_id, set())
    if not items:
        await message.reply("Список пуст.")
        return
    msg = "Ваш список покупок:\n" + "\n".join(f"- {i}" for i in items)
    await message.reply(msg)

@dp.message_handler(commands=['remove'])
async def remove_item(message: types.Message):
    user_id = message.from_user.id
    item = message.get_args()
    if not item:
        await message.reply("Что удалить? Используй: /remove товар")
        return
    if user_id in shopping_lists and item in shopping_lists[user_id]:
        shopping_lists[user_id].remove(item)
        await message.reply(f"Удалено: {item}")
    else:
        await message.reply("Такого товара нет в списке.")

@dp.message_handler(commands=['done'])
async def done_item(message: types.Message):
    user_id = message.from_user.id
    item = message.get_args()
    if not item:
        await message.reply("Что отметить купленным? Используй: /done товар")
        return
    if user_id in shopping_lists and item in shopping_lists[user_id]:
        shopping_lists[user_id].remove(item)
        await message.reply(f"Отмечено купленным: {item}")
    else:
        await message.reply("Такого товара нет в списке.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)