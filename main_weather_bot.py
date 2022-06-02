import requests
import datetime
import logging
from aiogram import Bot, Dispatcher, executor, types
from config import open_weather_token, tg_token

bot  = Bot(token = tg_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Привет напиши название города и я отправлю сводку по погоде!")

@dp.message_handler()
async def send_welcome(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    
    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric'
        )
        data = r.json()
        city = data['name']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно, не пойму что там за погода'
        humidity= data['main']['humidity']
        pressure= data['main']['pressure']
        cur_temp= data['main']['temp']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])

        await message.reply(
              f'***{datetime.datetime.now().strftime("%H:%M - %m.%d.%Y года")}***\n'
              f'Погода в городе: {city}\nТемпература: {cur_temp}C° {wd}\n'
              f'Атмосферное давление: {pressure} мм.рт.ст\nВлажность: {humidity} %\n'
              f'Скорось ветра: {wind} м/с\nВосход солнца: {sunrise_timestamp}\n'
              f'***Хорошего дня!***')
    except:
        await message.reply('\U00002620 Проверьте название города \U00002620')

if __name__ == '__main__':
    executor.start_polling(dp)