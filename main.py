import requests
import json
import datetime
from pprint import pprint
from config import open_weather_token

def get_weather (city, open_weather_token):
    
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
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric'
        )
        data = r.json()
        # pprint (data)
        
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

        print(
              f'***{datetime.datetime.now().strftime("%H:%M - %m.%d.%Y года")}***\n'
              f'Погода в городе: {city}\nТемпература: {cur_temp}C° {wd}\n'
              f'Атмосферное давление: {pressure} мм.рт.ст\nВлажность: {humidity} %\n'
              f'Скорось ветра: {wind} м/с\nВосход солнца: {sunrise_timestamp}\n'
              f'Хорошего дня!')
    except Exception as ex:
        print(ex)
        print('Проверьте название города')


def main():
    city  = input('Введите город: ')
    get_weather(city, open_weather_token)

if __name__ == '__main__':
    main()