import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from config_reader import config
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value())
# Диспетчер
dp = Dispatcher()
mylist = []


async def cmd_start(message: types.Message):
    await message.answer("Hiiiii! ^_^")


async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


async def cmd_test1(message: types.Message):
    await message.reply("Test 1")


async def cmd_test2(message: types.Message):
    await message.reply("Test 2")


@dp.message(commands=["create_list"])
async def cmd_create_list(message: types.Message):
    mylist = []
    await message.answer("Список создан")


@dp.message(commands=["add_to_list"])
async def cmd_add_to_list(message: types.Message, number: int):
    mylist.append(number)
    await message.answer("Добавлено число", number)


@dp.message(commands=["show_list"])
async def cmd_show_list(message: types.Message):
    await message.answer(f"Ваш список: {mylist}")


@dp.message(commands=["clear_list"])
async def cmd_clear_list(message: types.Message):
    mylist.clear()
    await message.answer("Список очищен")

# Запуск процесса поллинга новых апдейтов


async def main():
    dp.message.register(cmd_start, commands=["start"])
    dp.message.register(cmd_dice, commands=["dice"])
    dp.message.register(cmd_test1, commands=["test1"])
    dp.message.register(cmd_test2, commands=["test2"])
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
