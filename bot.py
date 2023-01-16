import asyncio
import logging
from datetime import datetime, timedelta
from aiohttp import BasicAuth
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.methods import send_location
from pyowm import OWM
f = open("info.txt", "r")
array = f.readlines()
LOGIN = str(array[0].rstrip())
PASSWORD = str(array[1].rstrip())
PROXY_URL = str(array[2].rstrip())
BOT_TOKEN = str(array[3].rstrip())
API_KEY = str(array[4].rstrip())
f.close()
logging.basicConfig(level=logging.INFO)
auth = BasicAuth(LOGIN, PASSWORD)
session = AiohttpSession(proxy=(PROXY_URL, auth))
bot = Bot(token=BOT_TOKEN, session=session)
# bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
mylist = []
table = [["Monday", "9:00", "10:00", "303", "Shilov", "differential equations"],
         ["Monday", "10:40", "12:10", "108", "Zouev", "intro to programming"],
         ["Tuesday", "12:00", "13:30", "303", "Shilov", "differential equations"],
         ["Saturday", "14:00", "15:30", "319",
             "Gorodetskiy", "Mathematical analysis"],
         ["Saturday", "21:00", "22:30", "303", "Shilov", "differential equations"],
         ["Sunday", "10:00", "11:30", "319", "Gorodetskiy", "Mathematical analysis"],
         ["Sunday", "12:00", "13:30", "303", "Shilov", "differential equations"],
         ["Sunday", "18:00", "19:30", "319", "Gorodetskiy", "Mathematical analysis"],]
weekdays = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]


@dp.message(commands=["date"])
async def cmd_date(message: types.Message):
    newdate = datetime.now()+timedelta(hours=3)
    newdate = newdate.strftime("%d.%m.%Y")
    await message.answer("Today is " + newdate)


@dp.message(commands=["time"])
async def cmd_time(message: types.Message):
    newtime = datetime.now()+timedelta(hours=3)
    newtime = newtime.strftime("%H:%M:%S")
    await message.answer("Now is " + newtime)


@dp.message(commands=["dice"])
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


@dp.message(commands=["start"])
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    # if message.from_user.id in (1, 1847234646):
    builder.add(types.InlineKeyboardButton(
        text="NEXT", callback_data="next_value"),
        types.InlineKeyboardButton(
        text="TODAY", callback_data="today_value"),
        types.InlineKeyboardButton(
        text="TOMORROW", callback_data="tomorrow_value"),)
    await message.answer("BS21-SD-01 Schedule", reply_markup=builder.as_markup())
    # else:
    #     await message.answer("You are not me >:(")


@dp.callback_query(text="next_value")
async def send_next_value(callback: types.CallbackQuery):
    newtime = datetime.now()+timedelta(hours=3)
    pairs = False
    for i in range(len(table)):
        if newtime.strftime("%A") == table[i][0] and newtime.strftime("%H:%M") < table[i][1]:
            pairs = True
            msg = table[i][0]+"\n"+table[i][5]+"\n"+table[i][4] + \
                "\n"+table[i][3]+"\n"+table[i][1] + \
                " - "+table[i][2]+"\n\n"+"/start"
            await callback.message.answer(msg)
            break
    if pairs == False:
        await callback.message.answer("No classes left 🎉")
    await callback.answer()


@dp.callback_query(text="today_value")
async def send_today_value(callback: types.CallbackQuery):
    today_string = ""
    newdate = datetime.now()+timedelta(hours=3)
    for i in range(len(table)):
        if newdate.strftime("%A") == table[i][0]:
            today_string += table[i][0]+"\n"+table[i][5]+"\n" + \
                table[i][4]+"\n"+table[i][3]+"\n" + \
                table[i][1]+" - "+table[i][2]+"\n\n"
    today_string += "/start"
    if today_string == "/start":
        await callback.message.answer("No classes today 🎉")
    else:
        await callback.message.answer(today_string)
    await callback.answer()


@dp.callback_query(text="tomorrow_value")
async def send_tmrw_value(callback: types.CallbackQuery):
    tomorrow_string = ""
    newdate = datetime.now()+timedelta(hours=3)
    tmrw = ""
    for i in range(len(weekdays)):
        if newdate.strftime("%A") == weekdays[i] and i == len(weekdays)-1:
            tmrw = weekdays[0]
        elif newdate.strftime("%A") == weekdays[i]:
            tmrw = weekdays[i+1]
    for i in range(len(table)):
        if tmrw == table[i][0]:
            tomorrow_string += table[i][0]+"\n"+table[i][5]+"\n" + \
                table[i][4]+"\n"+table[i][3]+"\n" + \
                table[i][1]+" - "+table[i][2]+"\n\n"
    tomorrow_string += "/start"
    if tomorrow_string == "/start":
        await callback.message.answer("No classes tomorrow 🎉")
    else:
        await callback.message.answer(tomorrow_string)
    await callback.answer()


@dp.message(commands=["test"])
async def cmd_test1(message: types.Message):
    await message.reply("Test")


@dp.message(commands=["name"])
async def cmd_name(message: types.Message, command: CommandObject):
    if command.args:
        await message.answer("Hello, " + command.args+"!")
    else:
        await message.answer("Please write your name after /name")


@dp.message(commands=["weather"])
async def cmd_weather(message: types.Message, command: CommandObject):
    if command.args:
        owm = OWM(API_KEY)
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(command.args)
        w = observation.weather
        temp = w.temperature('celsius')["temp"]
        await message.answer(f"In {command.args} is currently {w.detailed_status}.\nAir temperature: {temp}°C")
    else:
        await message.answer("Please write your city after /weather")


@dp.message(content_types=['location'])
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    owm = OWM(API_KEY)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_coords(lat, lon)
    w = observation.weather
    temp = w.temperature('celsius')["temp"]
    await message.answer(f"Air temperature at latitude: {lat},longitude: {lon}: \n{temp}°C")


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
