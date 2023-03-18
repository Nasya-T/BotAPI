import requests
import telebot
import random
from telebot import types
from bs4 import BeautifulSoup as b
import json

url = "https://www.anekdot.ru/last/good/"
def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    anekdots = soup.find_all('div', class_='text')
    return  [c.text for c in anekdots]
list_of_jokes = parser(url)
random.shuffle(list_of_jokes)

bot = telebot.TeleBot("5811437084:AAGl4OsAWawf24QfzhqJAQk0TO857dl_a7E", parse_mode=None)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Random_Dog 🐶')
    itembtn2 = types.KeyboardButton('Joke ⭐')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!'.format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def send_message(message):
    if message.text == 'Random_Dog 🐶':
        response = requests.get("https://random.dog/woof.json")
        data = json.loads(response.text)
        bot.send_message(message.chat.id, data['url'])
    if message.text == 'Joke ⭐':
        bot.send_message(message.chat.id,"------ АНЕКДОТ ------ \n"+list_of_jokes[0])
        del list_of_jokes[0]

bot.infinity_polling()