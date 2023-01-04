import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from config_reader import config
from aiogram.dispatcher.filters import CommandObject
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value())
# Диспетчер
dp = Dispatcher()
mylist = []


async def cmd_start(message: types.Message):
    await message.answer("Hi I'm HelperBot\nPowered by aiogram.")


async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


async def cmd_test1(message: types.Message):
    await message.reply("Test 1")


async def cmd_test2(message: types.Message):
    await message.reply("Test 2")


@dp.message(commands=["create"])
async def cmd_create(message: types.Message):
    mylist = []
    await message.answer("Список создан")


@dp.message(commands=["add"])
async def cmd_add(message: types.Message, command: CommandObject):
    if command.args:
        mylist.append(command.args)
        await message.answer("Добавлено число " + command.args + " в список")
    else:
        await message.answer("Пожалуйста, укажи число после команды /add")


@dp.message(commands=["show"])
async def cmd_show(message: types.Message):
    await message.answer(f"Ваш список: {mylist}")


@dp.message(commands=["remove"])
async def cmd_remove(message: types.Message, command: CommandObject):
    if command.args and command.args in mylist:
        mylist.remove(command.args)
        await message.answer("Удалено число " + command.args + " из списка")
    else:
        if command.args:
            await message.answer("Число " + command.args + " не найдено в списке")
        else:
            await message.answer("Пожалуйста, укажи число после команды /remove")


@dp.message(commands=["name"])
async def cmd_name(message: types.Message, command: CommandObject):
    if command.args:
        await message.answer("Привет, " + command.args+"!")
    else:
        await message.answer("Пожалуйста, укажи своё имя после команды /name")


@dp.message(commands=["clear"])
async def cmd_clear(message: types.Message):
    mylist.clear()
    await message.answer("Список очищен")


async def main():
    dp.message.register(cmd_start, commands=["start"])
    dp.message.register(cmd_dice, commands=["dice"])
    dp.message.register(cmd_test1, commands=["test1"])
    dp.message.register(cmd_test2, commands=["test2"])
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
