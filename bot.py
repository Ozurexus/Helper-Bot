import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from config_reader import config
from aiogram.dispatcher.filters import CommandObject, Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from random import randint

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
# Диспетчер
dp = Dispatcher()
mylist = []


# @dp.message(commands="start")
# async def cmd_start(message: types.Message):
#     kb = [
#         [types.KeyboardButton(text="NOW")],
#         [types.KeyboardButton(text="TODAY")],
#         [types.KeyboardButton(text="TOMORROW")],
#     ]
#     keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
#     await message.answer("WHEN?", reply_markup=keyboard)


# @dp.message(Text(text="NOW"))
# async def cmd_now(message: types.Message):
#     await message.reply("Шилов")


# @dp.message(Text(text="TODAY"))
# async def cmd_today(message: types.Message):
#     await message.reply("Шилов + Городецкий")


# @dp.message(Text(text="TOMORROW"))
# async def cmd_tmrw(message: types.Message):
#     await message.reply("Зуев", reply_markup=types.ReplyKeyboardRemove())


@dp.message(commands=["dice"])
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


@dp.message(commands=["random"])
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Нажми меня",
        callback_data="random_value")
    )
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил число от 1 до 10",
        reply_markup=builder.as_markup()
    )


@dp.message(commands=["NOW"])
async def cmd_now(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="NOW", callback_data="now_value"),
                types.InlineKeyboardButton(
                    text="TODAY", callback_data="today_value"),
                types.InlineKeyboardButton(
                    text="TOMORROW", callback_data="tomorrow_value"),
                )
    await message.answer(
        "Click the button",
        reply_markup=builder.as_markup()
    )


@dp.callback_query(text="random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))
    # await call.answer()


@dp.callback_query(text="now_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Шилов")
    # await callback.answer(
    #     text="Спасибо, что воспользовались ботом!",
    #     show_alert=True
    # )
    await callback.answer()


@dp.callback_query(text="today_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Шилов + Городецкий")
    await callback.answer()


@dp.callback_query(text="tomorrow_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Зуев")
    await callback.answer()


@dp.message(commands=["test1"])
async def cmd_test1(message: types.Message):
    await message.reply("Test 1")


@dp.message(commands=["test2"])
async def cmd_test2(message: types.Message):
    await message.reply("Test 2")


@dp.message(commands=["name"])
async def cmd_name(message: types.Message, command: CommandObject):
    if command.args:
        await message.answer("Привет, " + command.args+"!")
    else:
        await message.answer("Пожалуйста, укажи своё имя после команды /name")


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


@dp.message(commands=["list"])
async def cmd_list(message: types.Message):
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


@dp.message(commands=["clear"])
async def cmd_clear(message: types.Message):
    mylist.clear()
    await message.answer("Список очищен")


@dp.message(content_types="text")
async def echo(message: types.Message):
    await message.answer(message.text)
# async def extract_data(message: types.Message):
#     data = {
#         "url": "<N/A>",
#         "email": "<N/A>",
#         "code": "<N/A>"
#     }
#     entities = message.entities or []
#     for item in entities:
#         if item.type in data.keys():
#             data[item.type] = item.extract(message.text)
#     await message.reply(
#         "Вот что я нашёл:\n"
#         f"URL: {html.quote(data['url'])}\n"
#         f"E-mail: {html.quote(data['email'])}\n"
#         f"Пароль: {html.quote(data['code'])}"
#     )


@dp.message(content_types=[types.ContentType.ANIMATION])
async def echo_gif(message: types.Message):
    await message.reply_animation(message.animation.file_id)


@dp.message(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def somebody_added(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(f"Привет, {user.full_name}")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
