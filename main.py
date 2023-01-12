
import os
import telebot, re
import json
from difflib import SequenceMatcher

TOKEN = "5433379156:AAGu2v4NXjC677CZPzpVWmob-Yja-rbD6Po"
threshold = 0.5

################################################################################

def save_dict(dict, name):
    json.dump(dict, open(str(name) + '.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

def read_dict(name):
    with open(str(name) + '.json', encoding='utf-8') as fh:
        data = json.load(fh)
    return data

################################################################################

ticket_dict = {}
try:
    ticket_dict = read_dict('tickets')['tickets']
except Exception as e:
    print("READ ERROR:", e)

# нахождение вопроса
def get_ticket(answer):
    percent_arr = []
    for ticket in ticket_dict:
        percent = SequenceMatcher(lambda x: x==" ", answer, ticket['question'].split(":")[1][1:]).ratio()
        percent_arr.append([ticket, percent])

    percent_arr.sort(key=lambda val: val[1], reverse=True)
    return percent_arr[0][0]['answer'], percent_arr[0][1]

################################################################################

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Напишите вопрос из билета.')

@bot.message_handler(content_types=["text"])
def handle_text(message):
    answer = get_ticket(message.text)
    bot.send_message(message.chat.id, "Совпадение %.2f%% \n%s" % (answer[1] * 100, answer[0]))

bot.polling(none_stop=True, interval=0)
