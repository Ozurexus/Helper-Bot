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
# logging.basicConfig(level=logging.INFO)
# auth = BasicAuth(LOGIN, PASSWORD)
# session = AiohttpSession(proxy=(PROXY_URL, auth))
# bot = Bot(token=BOT_TOKEN, session=session)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
mylist = []
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
             "System and Network Administration (lec))"],
         ["Friday", "13:00", "14:30", "101", "Awwal Ishiaku",
         "System and Network Administration (lab)"],]

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


@dp.message(commands=["idtest"])
async def cmd_idtest(message: types.Message):
    msg = "Your id is "+str(message.from_user.id)
    await message.answer(msg)


@dp.message(commands=["start"])
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="NEXT", callback_data="next_value"),
        types.InlineKeyboardButton(
        text="TODAY", callback_data="today_value"),
        types.InlineKeyboardButton(
        text="TOMORROW", callback_data="tomorrow_value"),
        types.InlineKeyboardButton(
        text="WEEK", callback_data="choose_value"),
    )
    await message.answer("BS21-SD-01 Schedule:", reply_markup=builder.as_markup())


@dp.callback_query(text="next_value")  # TODO refactor
async def send_next_value(callback: types.CallbackQuery):
    newtime = datetime.now() + timedelta(hours=3)
    next = False
    ongoing = False
    weekday = False
    msg = ''
    for i in range(len(table)):
        if newtime.strftime("%A") == table[i][0]:
            if weekday == False:
                msg += table[i][0]+":\n"
                weekday = True
            msg += table[i][5]+"\n"+table[i][4] + \
                "\n"+table[i][3]+"\n"+table[i][1] + \
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
        await callback.message.answer("No classes left 🎉")
    else:
        msg += "/start"
        await callback.message.answer(msg)
    await callback.answer()


@dp.callback_query(text="today_value")
async def send_today_value(callback: types.CallbackQuery):
    today_string = ""
    weekday = False
    newdate = datetime.now()+timedelta(hours=3)
    for i in range(len(table)):
        if newdate.strftime("%A") == table[i][0]:
            if weekday == False:
                today_string += table[i][0]+":\n"
                weekday = True
            today_string += table[i][5]+"\n" + \
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
    weekday = False
    for i in range(len(weekdays)):
        if newdate.strftime("%A") == weekdays[i] and i == len(weekdays)-1:
            tmrw = weekdays[0]
        elif newdate.strftime("%A") == weekdays[i]:
            tmrw = weekdays[i+1]
    for i in range(len(table)):
        if tmrw == table[i][0]:
            if weekday == False:
                tomorrow_string += table[i][0]+":\n"
                weekday = True
            tomorrow_string += table[i][5]+"\n" + \
                table[i][4]+"\n"+table[i][3]+"\n" + \
                table[i][1]+" - "+table[i][2]+"\n\n"
    tomorrow_string += "/start"
    if tomorrow_string == "/start":
        await callback.message.answer("No classes tomorrow 🎉")
    else:
        await callback.message.answer(tomorrow_string)
    await callback.answer()


@dp.callback_query(text="choose_value")
async def send_choose_value(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="MONDAY", callback_data="monday_value"),
        types.InlineKeyboardButton(
        text="TUESDAY", callback_data="tuesday_value"),
        types.InlineKeyboardButton(
        text="WEDNESDAY", callback_data="wednesday_value"),
        types.InlineKeyboardButton(
        text="THURSDAY", callback_data="thursday_value"),
        types.InlineKeyboardButton(
        text="FRIDAY", callback_data="friday_value"),
    )
    await callback.message.answer("Choose a weekday:", reply_markup=builder.as_markup())


@dp.callback_query(text="monday_value")
async def send_monday_value(callback: types.CallbackQuery):
    monday_string = ""
    weekday = False
    for i in range(len(table)):
        if "Monday" == table[i][0]:
            if weekday == False:
                monday_string += table[i][0]+":\n"
                weekday = True
            monday_string += table[i][5]+"\n" + \
                table[i][4]+"\n"+table[i][3]+"\n" + \
                table[i][1]+" - "+table[i][2]+"\n\n"
    monday_string += "/start"
    if monday_string == "/start":
        await callback.message.answer("No classes on Monday 🎉")
    else:
        await callback.message.answer(monday_string)
    await callback.answer()


@dp.callback_query(text="tuesday_value")
async def send_tuesday_value(callback: types.CallbackQuery):
    tuesday_string = ""
    weekday = False
    for i in range(len(table)):
        if "Tuesday" == table[i][0]:
            if weekday == False:
                tuesday_string += table[i][0]+":\n"
                weekday = True
            tuesday_string += table[i][5]+"\n" + \
                table[i][4]+"\n"+table[i][3]+"\n" + \
                table[i][1]+" - "+table[i][2]+"\n\n"
    tuesday_string += "/start"
    if tuesday_string == "/start":
        await callback.message.answer("No classes on Tuesday 🎉")
    else:
        await callback.message.answer(tuesday_string)
    await callback.answer()


@dp.callback_query(text="wednesday_value")
async def send_wednesday_value(callback: types.CallbackQuery):
    wednesday_string = ""
    weekday = False
    for i in range(len(table)):
        if "Wednesday" == table[i][0]:
            if weekday == False:
                wednesday_string += table[i][0]+":\n"
                weekday = True
            wednesday_string += table[i][5]+"\n" + \
                table[i][4]+"\n"+table[i][3]+"\n" + \
                table[i][1]+" - "+table[i][2]+"\n\n"
    wednesday_string += "/start"
    if wednesday_string == "/start":
        await callback.message.answer("No classes on Wednesday 🎉")
    else:
        await callback.message.answer(wednesday_string)
    await callback.answer()


@dp.callback_query(text="thursday_value")
async def send_thursday_value(callback: types.CallbackQuery):
    thursday_string = ""
    weekday = False
    for i in range(len(table)):
        if "Thursday" == table[i][0]:
            if weekday == False:
                thursday_string += table[i][0]+":\n"
                weekday = True
            thursday_string += table[i][5]+"\n" + \
                table[i][4]+"\n"+table[i][3]+"\n" + \
                table[i][1]+" - "+table[i][2]+"\n\n"
    thursday_string += "/start"
    if thursday_string == "/start":
        await callback.message.answer("No classes on Thursday 🎉")
    else:
        await callback.message.answer(thursday_string)
    await callback.answer()


@dp.callback_query(text="friday_value")
async def send_friday_value(callback: types.CallbackQuery):
    friday_string = ""
    weekday = False
    for i in range(len(table)):
        if "Friday" == table[i][0]:
            if weekday == False:
                friday_string += table[i][0]+":\n"
                weekday = True
            friday_string += table[i][5]+"\n" + \
                table[i][4]+"\n"+table[i][3]+"\n" + \
                table[i][1]+" - "+table[i][2]+"\n\n"
    friday_string += "/start"
    if friday_string == "/start":
        await callback.message.answer("No classes on Friday 🎉")
    else:
        await callback.message.answer(friday_string)
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


# @ dp.message(content_types=['sendloco'])
# async def handle_location(message: types.Message):
#     pass


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
