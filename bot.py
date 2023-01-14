import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import BasicAuth
from aiogram.client.session.aiohttp import AiohttpSession
f = open("info.txt", "r")
array = f.readlines()
LOGIN = str(array[0].rstrip())
PASSWORD = str(array[1].rstrip())
BOT_TOKEN = str(array[2].rstrip())
PROXY_URL = str(array[3].rstrip())
f.close()
logging.basicConfig(level=logging.INFO)
auth = BasicAuth(LOGIN, PASSWORD)
session = AiohttpSession(proxy=(PROXY_URL, auth))
bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()
mylist = []
t = [["Monday", "9:00", "10:00", "303", "Shilov", "differential equations"],
     ["Monday", "10:40", "12:10", "108", "Zouev", "intro to programming"],
     ["Tuesday", "12:00", "13:30", "303", "Shilov", "differential equations"],
     ["Saturday", "14:00", "15:30", "319", "Gorodetskiy", "Mathematical analysis"],
     ["Saturday", "21:00", "22:30" "303", "Shilov", "differential equations"],
     ["Sunday", "10:00", "11:30", "319", "Gorodetskiy", "Mathematical analysis"],
     ["Sunday", "12:00", "13:30", "303", "Shilov", "differential equations"],
     ["Sunday", "18:00", "19:30", "319", "Gorodetskiy", "Mathematical analysis"],]
# increase all hours by 3
# for i in range(len(t)):
#     t[i][1] = str(int(t[i][1][:2]) + 3) + t[i][1][2:]
#     t[i][2] = str(int(t[i][2][:2]) + 3) + t[i][2][2:]
weekdays = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]


@dp.message(commands=["date"])
async def cmd_date(message: types.Message):
    newdate = datetime.now()
    newdate = newdate.strftime("%d.%m.%Y")
    await message.answer("Today is " + newdate)


@dp.message(commands=["time"])
async def cmd_time(message: types.Message):
    newtime = datetime.now()
    newtime = newtime.strftime("%H:%M:%S")
    await message.answer("Now is " + newtime)


@dp.message(commands=["dice"])
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


@dp.message(commands=["now"])
async def cmd_now(message: types.Message):
    builder = InlineKeyboardBuilder()
    # if message.from_user.id in (1, 1847234646):
    builder.add(types.InlineKeyboardButton(
        text="NEXT", callback_data="next_value"),
        types.InlineKeyboardButton(
        text="TODAY", callback_data="today_value"),
        types.InlineKeyboardButton(
        text="TOMORROW", callback_data="tomorrow_value"),)
    await message.answer("Click the button", reply_markup=builder.as_markup())
    # else:
    #     await message.answer("You are not me >:(")


@dp.callback_query(text="next_value")
async def send_next_value(callback: types.CallbackQuery):
    newdate = datetime.now()
    pairs = False
    for i in range(len(t)):
        if newdate.strftime("%A") == t[i][0] and newdate.strftime("%H:%M") < t[i][1]:
            pairs = True
            msg = t[i][0]+"\n"+t[i][5]+"\n"+t[i][4] + \
                "\n"+t[i][3]+"\n"+t[i][1]+" - "+t[i][2]
            await callback.message.answer(msg)
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
            today_string += t[i][0]+"\n"+t[i][5]+"\n" + \
                t[i][4]+"\n"+t[i][3]+"\n"+t[i][1]+" - "+t[i][2]+"\n\n"
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
            tomorrow_string += t[i][0]+"\n"+t[i][5]+"\n" + \
                t[i][4]+"\n"+t[i][3]+"\n"+t[i][1]+" - "+t[i][2]+"\n\n"
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
        await message.answer("Hello, " + command.args+"!")
    else:
        await message.answer("Please write your name after /name")


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
    await message.answer("I don't understand you")


@dp.message(content_types=[types.ContentType.ANIMATION])
async def echo_gif(message: types.Message):
    await message.reply_animation(message.animation.file_id)


@dp.message(content_types=[types.ContentType.STICKER])
async def echo_sticker(message: types.Message):
    await message.reply_sticker(message.sticker.file_id)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
