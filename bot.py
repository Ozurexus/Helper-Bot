import asyncio
import logging
from pyowm import OWM
from datetime import datetime, timedelta
from aiohttp import BasicAuth
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import CommandObject, Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.session.aiohttp import AiohttpSession
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest

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
day_data = {}
week_data = {}
users = []
table = [["Monday", "9:20", "10:50", "ONLINE", "Adil Khan",
          "Introduction to Machine Learning (lec)"],
         ["Monday", "13:00", "14:30", "317", "Roman Garaev",
             "Introduction to Machine Learning (lab)"],
         ["Tuesday", "11:00", "12:30", "ONLINE",
             "Darko Bozhinoski", "Databases (lec)"],
         ["Tuesday", "13:00", "14:30", "106",
             "Hamza Salem", "Databases (tut)"],
         ["Tuesday", "14:40", "16:10", "312",
             "Munir Makhmutov", "Databases (lab)"],
         ["Wednesday", "11:00", "12:30", "ONLINE",
             "Paolo Ciancarini", "Networks (lec)"],
         ["Wednesday", "13:00", "14:30", "105",
             "Artem Burmyakov", "Networks (tut)"],
         ["Wednesday", "14:40", "16:10", "314",
             "Gerald B. Imbugwa", "Networks (lab)"],
         ["Friday", "9:20", "10:50", "ONLINE", "Kirill Saltanov",
             "System and Network Administration (lec)"],
         ["Friday", "13:00", "14:30", "101", "Awwal Ishiaku",
         "System and Network Administration (lab)"],]

weekdays = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]


def get_keyboard():
    buttons = [[
        types.InlineKeyboardButton(text="NEXT", callback_data="day_next"),
        types.InlineKeyboardButton(
            text="TODAY", callback_data="day_today"),
        types.InlineKeyboardButton(
            text="TOMORROW", callback_data="day_tomorrow"),]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def update_day_text(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(new_value, reply_markup=get_keyboard())


@dp.message(commands=["start"])
async def cmd_days(message: types.Message):
    if message.from_user.id not in users:
        users.append(message.from_user.id)
    day_data[message.from_user.id] = 0
    await message.answer("BS21-SD-01 Schedule:", reply_markup=get_keyboard())


@dp.callback_query(Text(text_startswith="day_"))
async def callbacks_day(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    if action == "next":
        day_data[callback.from_user.id] = get_next()
    elif action == "today":
        day_data[callback.from_user.id] = get_today()
    elif action == "tomorrow":
        day_data[callback.from_user.id] = get_tomorrow()
    await update_day_text(callback.message, day_data[callback.from_user.id])
    await callback.answer()


def get_next():
    newtime = datetime.now() + timedelta(hours=3)
    next = False
    ongoing = False
    weekday = False
    msg = ''
    for i in range(len(table)):
        if newtime.strftime("%A") == table[i][0]:
            if weekday == False:
                msg += "--- "+str(table[i][0]).upper()+" ---\n"
                weekday = True
            msg += "📚" + table[i][5]+"\n🤓"+table[i][4] + \
                "\n🏠"+table[i][3]+"\n⏰"+table[i][1] + \
                " - "+table[i][2]+"\n"
            tmptime = newtime.strftime("%H:%M").split(":")
            tmptime = int(tmptime[0])*3600+int(tmptime[1])*60
            if table[i][1] < newtime.strftime("%H:%M") < table[i][2] and ongoing == False:
                ongoing = True
                ttime = table[i][2].split(":")
                ttime = int(ttime[0])*3600+int(ttime[1])*60
                diff = (ttime-tmptime)
                hourdiff = diff//3600
                mindiff = (diff % 3600)//60
                msg += "Time left: "+str(hourdiff)+":"+str(mindiff)+"\n\n"
            elif table[i][1] > newtime.strftime("%H:%M") and next == False:
                next = True
                ttime = table[i][1].split(":")
                ttime = int(ttime[0])*3600+int(ttime[1])*60
                diff = (ttime-tmptime)
                hourdiff = diff//3600
                mindiff = (diff % 3600)//60
                msg += "Time until: "+str(hourdiff)+":"+str(mindiff)+"\n\n"
    if next == False and ongoing == False:
        msg = "No classes left 🎉"
    return (msg)


def get_today():
    msg = ""
    weekday = False
    newdate = datetime.now()+timedelta(hours=3)
    for i in range(len(table)):
        if newdate.strftime("%A") == table[i][0]:
            if weekday == False:
                msg += "--- "+str(table[i][0]).upper()+" ---\n"
                weekday = True
            msg += "📚" + table[i][5]+"\n🤓"+table[i][4] + \
                "\n🏠"+table[i][3]+"\n⏰"+table[i][1] + \
                " - "+table[i][2]+"\n\n"
    if msg == '':
        msg = "No classes today 🎉"
    return (msg)


def get_tomorrow():
    msg = ""
    newdate = datetime.now()+timedelta(hours=3)
    tmrw = ""
    weekday = False
    for i in range(len(weekdays)):
        if newdate.strftime("%A") == weekdays[i] and i == len(weekdays)-1:
            tmrw = weekdays[0]
        elif newdate.strftime("%A") == weekdays[i]:
            tmrw = weekdays[i+1]
    for i in range(len(table)):
        if tmrw == table[i][0]:
            if weekday == False:
                msg += "--- "+str(table[i][0]).upper()+" ---\n"
                weekday = True
            msg += "📚" + table[i][5]+"\n🤓"+table[i][4] + \
                "\n🏠"+table[i][3]+"\n⏰"+table[i][1] + \
                " - "+table[i][2]+"\n\n"
    if msg == '':
        msg = "No classes tomorrow 🎉"
    return msg


def get_keyboard2():
    buttons = [[types.InlineKeyboardButton(text="MONDAY", callback_data="week_monday"),
                types.InlineKeyboardButton(
                    text="TUESDAY", callback_data="week_tuesday"),
                types.InlineKeyboardButton(text="WEDNESDAY", callback_data="week_wednesday")],
               [types.InlineKeyboardButton(text="THURSDAY", callback_data="week_thursday"),
                types.InlineKeyboardButton(
                    text="FRIDAY", callback_data="week_friday"),
                types.InlineKeyboardButton(text="SATURDAY", callback_data="week_saturday")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@dp.message(commands=["week"])
async def cmd_week(message: types.Message):
    if message.from_user.id not in users:
        users.append(message.from_user.id)
    week_data[message.from_user.id] = 0
    await message.answer("BS21-SD-01 Schedule for a week:", reply_markup=get_keyboard2())


@dp.callback_query(Text(text_startswith="week_"))
async def callbacks_week(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    week_data[callback.from_user.id] = get_day(action.capitalize())
    await update_week_text(callback.message, week_data[callback.from_user.id])
    await callback.answer()


def get_day(day):
    msg = ""
    weekday = False
    for i in range(len(table)):
        if day == table[i][0]:
            if weekday == False:
                msg += "--- "+str(table[i][0]).upper()+" ---\n"
                weekday = True
            msg += "📚" + table[i][5]+"\n🤓"+table[i][4] + \
                "\n🏠"+table[i][3]+"\n⏰"+table[i][1] + \
                " - "+table[i][2]+"\n\n"
    if msg == "":
        msg = "No classes on "+str(day)+"🎉"
    return msg


async def update_week_text(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(new_value, reply_markup=get_keyboard2())


@dp.message(commands=["show"])
async def cmd_show(message: types.Message):
    if message.from_user.id == 1847234646:
        msg = ''
        if len(users) == 0:
            msg = "No users"
        else:
            for i in range(len(users)):
                msg += str(users[i])+'\n'
        await message.answer(msg)
    else:
        await message.answer("You are not authorized to use this command.")


@dp.message(commands=["cleanup"])
async def cmd_cleanup(message: types.Message):
    if message.from_user.id == 1847234646:
        msg = ''
        for i in day_data:
            msg += str(i)+': '+str(day_data[i])+'\n'
        await message.answer(msg)
        day_data.clear()
        msg = ''
        for i in week_data:
            msg += str(i)+': '+str(week_data[i])+'\n'
        await message.answer(msg)
        week_data.clear()
    else:
        await message.answer("You are not authorized to use this command.")


@ dp.message(commands=["delete"])
async def cmd_delete(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)


@ dp.message(commands=["date"])
async def cmd_date(message: types.Message):
    newdate = datetime.now()+timedelta(hours=3)
    newdate = newdate.strftime("%d.%m.%Y")
    await message.answer("Today is " + newdate)


@ dp.message(commands=["time"])
async def cmd_time(message: types.Message):
    newtime = datetime.now()+timedelta(hours=3)
    newtime = newtime.strftime("%H:%M:%S")
    await message.answer("Now is " + newtime)


@ dp.message(commands=["dice"])
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


@ dp.message(commands=["id"])
async def cmd_id(message: types.Message):
    msg = "Your id is "+str(message.from_user.id)
    await message.answer(msg)


@ dp.message(commands=["name"])
async def cmd_name(message: types.Message, command: CommandObject):
    if command.args:
        await message.answer("Hello, " + command.args+"!")
    else:
        await message.answer("Please write your name after /name")


@ dp.message(commands=["weather"])
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
    lat = round(message.location.latitude, 3)
    lon = round(message.location.longitude, 3)
    owm = OWM(API_KEY)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_coords(lat, lon)
    w = observation.weather
    temp = w.temperature('celsius')["temp"]
    await message.answer(f"Air temperature at latitude {lat}, longitude {lon}, is {temp}°C.")


@dp.message(content_types="text")
async def echo(message: types.Message):
    print("\n", message.text, "\n")
    await message.answer("I don't understand you, human.")


@ dp.message(content_types=[types.ContentType.ANIMATION])
async def echo_gif(message: types.Message):
    await message.reply_animation(message.animation.file_id)


@ dp.message(content_types=[types.ContentType.STICKER])
async def echo_sticker(message: types.Message):
    await message.reply_sticker(message.sticker.file_id)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
