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
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State

f = open("info.txt", "r")
array = f.readlines()
LOGIN = str(array[0].rstrip())
PASSWORD = str(array[1].rstrip())
PROXY_URL = str(array[2].rstrip())
BOT_TOKEN = str(array[3].rstrip())
API_KEY = str(array[4].rstrip())
f.close()

f = open("extra.txt", "r")
users = []
for line in f:
    users.append(line.strip())
f.close()
users = set(users)
users = list(users)

logging.basicConfig(level=logging.INFO)
auth = BasicAuth(LOGIN, PASSWORD)
session = AiohttpSession(proxy=(PROXY_URL, auth))
bot = Bot(token=BOT_TOKEN, session=session)

# bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()
day_data = {}
week_data = {}
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
         ["Friday", "14:40", "16:10", "101", "Awwal Ishiaku",
         "System and Network Administration (lab)"]]

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


def file_mod(users):
    f = open("extra.txt", "r")
    array = f.readlines()
    for i in range(len(array)):
        array[i] = (array[i].rstrip('\n'))
    array = set(array)
    users = set(users)
    array = users | array
    array = list(array)
    f.close()
    f = open("extra.txt", "w")
    for i in range(len(array)):
        f.write(str(array[i])+'\n')
    f.close()
    return


@dp.message(commands=["start"])
async def cmd_days(message: types.Message):
    if message.from_user.id not in users:
        users.append(message.from_user.id)
        file_mod(users)
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


def cmpr(time1, time2):
    time1 = time1.split(":")
    time2 = time2.split(":")
    if int(time1[0]) > int(time2[0]):
        return True
    elif int(time1[0]) == int(time2[0]):
        if int(time1[1]) > int(time2[1]):
            return True
        else:
            return False
    else:
        return False


def get_next():
    newtime = datetime.now() + timedelta(hours=3)
    next = False
    ongoing = False
    weekday = False
    msg = ''
    for i in range(len(table)):
        if newtime.strftime("%A") == table[i][0]:
            if not cmpr(table[i][1], newtime.strftime("%H:%M")) and not cmpr(newtime.strftime("%H:%M"), table[i][2]) and ongoing == False:
                if weekday == False:
                    msg += "--- "+str(table[i][0]).upper()+" ---\n"
                    weekday = True
                msg += "📚" + table[i][5]+"\n🤓"+table[i][4] + \
                    "\n🏠"+table[i][3]+"\n⏰"+table[i][1] + \
                    " - "+table[i][2]+"\n"
                tmptime = newtime.strftime("%H:%M").split(":")
                tmptime = int(tmptime[0])*3600+int(tmptime[1])*60
                ongoing = True
                ttime = table[i][2].split(":")
                ttime = int(ttime[0])*3600+int(ttime[1])*60
                diff = (ttime-tmptime)
                hourdiff = diff//3600
                mindiff = (diff % 3600)//60
                if hourdiff < 10:
                    hourdiff = "0"+str(hourdiff)
                if mindiff < 10:
                    mindiff = "0"+str(mindiff)
                msg += "Time left: "+str(hourdiff)+":"+str(mindiff)+"\n\n"
            elif cmpr(table[i][1], newtime.strftime("%H:%M")) and next == False:
                if weekday == False:
                    msg += "--- "+str(table[i][0]).upper()+" ---\n"
                    weekday = True
                msg += "📚" + table[i][5]+"\n🤓"+table[i][4] + \
                    "\n🏠"+table[i][3]+"\n⏰"+table[i][1] + \
                    " - "+table[i][2]+"\n"
                tmptime = newtime.strftime("%H:%M").split(":")
                tmptime = int(tmptime[0])*3600+int(tmptime[1])*60
                next = True
                ttime = table[i][1].split(":")
                ttime = int(ttime[0])*3600+int(ttime[1])*60
                diff = ttime-tmptime
                hourdiff = diff//3600
                mindiff = (diff % 3600)//60
                if hourdiff < 10:
                    hourdiff = "0"+str(hourdiff)
                if mindiff < 10:
                    mindiff = "0"+str(mindiff)
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
        file_mod(users)
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


@dp.message(commands=["delete"])
async def cmd_delete(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message(commands=["time"])
async def cmd_fullnow(message: types.Message):
    now = datetime.now()+timedelta(hours=3)
    await message.answer(now.strftime("%d/%m/%Y %H:%M:%S"))


@dp.message(commands=["dice"])
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


@dp.message(commands=["id"])
async def cmd_id(message: types.Message):
    msg = "Your id is "+str(message.from_user.id)
    await message.answer(msg)


class WeatherStates(StatesGroup):
    start = State()
    finish = State()


@dp.message(commands=["weather"])
async def cmd_weather(message: types.Message, state: FSMContext):
    await message.answer("Please write your city")
    await state.set_state(WeatherStates.start)


@dp.message(state=WeatherStates.start)
async def cmd_weather(message: types.Message, state: FSMContext):
    owm = OWM(API_KEY)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(message.text)
    w = observation.weather
    temp = w.temperature('celsius')["temp"]
    await message.answer(f"In {message.text} is currently {w.detailed_status}.\nAir temperature: {temp}°C")
    await state.set_state(WeatherStates.finish)


class StipaStates(StatesGroup):
    start = State()
    finish = State()


@dp.message(commands=["stipa"])
async def cmd_stipa(message: types.Message, state: FSMContext):
    await message.answer("Please write your grades without spaces between them")
    await state.set_state(StipaStates.start)


@dp.message(state=StipaStates.start)
async def cmd_stipa(message: types.Message, state: FSMContext):
    msg = message.text.split()
    msg = list(msg[0])
    GPA = 0
    for i in range(len(msg)):
        match msg[i].upper():
            case 'A' | 'P':
                msg[i] = '5'
            case 'B':
                msg[i] = '4'
            case 'C':
                msg[i] = '3'
            case 'D' | 'F':
                msg[i] = '2'
        GPA += int(msg[i])
    GPA /= len(msg)
    Bmin = 3000
    Bmax = 20000
    Srac = 0
    S = Bmin+(Bmax-Bmin)*((GPA-2)/(5-2))**2.5-Srac
    S = (round(S)//100)*100
    Expenses = 3100
    await message.answer(f"Your GPA is {GPA}.\nYour stipend is {S} rubles.\nAfter expenses you will have {S-Expenses} rubles.")
    await state.set_state(StipaStates.finish)


@dp.message(commands=["links"])
async def cmd_links(message: types.Message):
    schedule = 'https://docs.google.com/spreadsheets/d/1wJtbTxo-ZPmBIt27BKQizwxtVM4_1sKA9vDyxGBAq-w/edit#gid=398810915'
    courses = 'https://docs.google.com/spreadsheets/d/1DZcxd6KA4BoZnEzw3BNFUz0QqO0DU3qE5VVD69yRHzc/edit?usp=sharing'
    syllabus = 'https://eduwiki.innopolis.university/index.php/BSc:Syllabi_Table_3+1'
    distribution = 'https://docs.google.com/spreadsheets/d/19u7D7cXOCAqj_CCCLFRxf54w5SWMcT_naC7LwiCD0PA/htmlview?usp=sharing#'
    msg = f"Schedule: {schedule}\nCourses: {courses}\nSyllabus: {syllabus}\nDistribution: {distribution}"
    if message.from_user.id == 1847234646:
        gdrive = 'https://drive.google.com/drive/folders/16qU6ABeNBWshTYqSw0XtLmAwPO2kD8NA'
        msg += f"\nGoogle Drive: {gdrive}"
    await message.answer(msg)


@dp.message(commands="send_loco")
async def callback_query(call: types.CallbackQuery):
    await call.message.answer("Send location", reply_markup=types.ReplyKeyboardRemove())


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
