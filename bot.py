import asyncio
import logging
from random import choice, randint
from config_reader import config
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import Message
from aiogram.dispatcher.filters import CommandObject, Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
dp = Dispatcher()
mylist = []
router = Router()
t = [["Monday", "9:00", "303", "Shilov"],
     ["Monday", "10:40", "108", "Zouev"],
     ["Tuesday", "12:00", "303", "Shilov"],
     ["Saturday", "14:00", "319", "Gorodetskiy"],
     ["Saturday", "21:00", "303", "Shilov"],
     ["Sunday", "10:00", "319", "Gorodetskiy"],
     ["Sunday", "12:00", "303", "Shilov"]]
weekdays = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]
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
@ dp.message(commands=["date"])
async def cmd_date(message: types.Message):
    newdate = datetime.now()
    newdate = newdate.strftime("%d.%m.%Y")
    await message.answer("Сегодня " + newdate)


@ dp.message(commands=["time"])
async def cmd_time(message: types.Message):
    newtime = datetime.now()
    newtime = newtime.strftime("%H:%M:%S")
    await message.answer("Сейчас " + newtime)


@ dp.message(commands=["dice"])
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


@ dp.message(commands=["random"])
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


@ dp.message(commands=["now"])
async def cmd_now(message: types.Message):
    builder = InlineKeyboardBuilder()
    # if message.from_user.id in (1, 1847234646):
    builder.add(types.InlineKeyboardButton(text="NEXT", callback_data="next_value"),
                types.InlineKeyboardButton(
                text="TODAY", callback_data="today_value"),
                types.InlineKeyboardButton(
                text="TOMORROW", callback_data="tomorrow_value"),
                )
    await message.answer(
        "Click the button",
        reply_markup=builder.as_markup()
    )
    # else:
    #     await message.answer("You are not me >:(")


@dp.callback_query(text="random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))
    await callback.answer()


@dp.callback_query(text="next_value")
async def send_next_value(callback: types.CallbackQuery):
    newdate = datetime.now()
    # await callback.answer(
    #     text="Спасибо, что воспользовались ботом!",
    #     show_alert=True
    # )
    pairs = False
    for i in range(len(t)):
        if newdate.strftime("%A") == t[i][0] and newdate.strftime("%H:%M") < t[i][1]:
            pairs = True
            await callback.message.answer(t[i][0] + "\n" + t[i][1] + "\n" + t[i][2] + "\n" + t[i][3])
            break
    if pairs == False:
        await callback.message.answer("No classes left 🎉")
    await callback.answer()


@dp.callback_query(text="today_value")
async def send_today_value(callback: types.CallbackQuery):
    today_string = ""
    newdate = datetime.now()
    for i in range(len(t)):
        if newdate.strftime("%A") == t[i][0]:
            today_string += t[i][0] + "\n" + t[i][1] + \
                "\n" + t[i][2] + "\n" + t[i][3] + "\n\n"
    if today_string == "":
        await callback.message.answer("No classes today 🎉")
    else:
        await callback.message.answer(today_string)
    await callback.answer()


@dp.callback_query(text="tomorrow_value")
async def send_tmrw_value(callback: types.CallbackQuery):
    tomorrow_string = ""
    newdate = datetime.now()
    tmrw = ""
    for i in range(len(weekdays)):
        if newdate.strftime("%A") == weekdays[i] and i == len(weekdays)-1:
            tmrw = weekdays[0]
        elif newdate.strftime("%A") == weekdays[i]:
            tmrw = weekdays[i+1]
    for i in range(len(t)):
        if tmrw == t[i][0]:
            tomorrow_string += t[i][0] + "\n" + t[i][1] + \
                "\n" + t[i][2] + "\n" + t[i][3] + "\n\n"
    if tomorrow_string == "":
        await callback.message.answer("No classes tomorrow 🎉")
    else:
        await callback.message.answer(tomorrow_string)
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
    print("\n", message.text, "\n")
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
