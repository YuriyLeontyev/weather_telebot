import telebot
import requests
import json
from config import BOT, APIKEY
bot = telebot.TeleBot(BOT)

API = APIKEY

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,'Введи назание города:')
    #bot.register_next_step_handler( message, get_weather)

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        wind = data["wind"]["speed"]
        pressure = data["main"]["pressure"]
        bot.reply_to(message, f'Температура: {temp} \n Ветер: {wind}\n Давление: {pressure}')

        image = 'warm.jpg' if temp >5.0 else 'cold.jpg'
        file = open('./' + image,'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, "Че за город? Пиши корректно!")


bot.infinity_polling()