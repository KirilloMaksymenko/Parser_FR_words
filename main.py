#project - Parser_FR_words , Author - Maksymenko Kyrylo

#"https://conjugator.reverso.net/conjugation-french-verb-{verb}.html"

from ast import Pass
import requests
import json
from bs4 import BeautifulSoup
import telebot

bot = telebot.TeleBot("5299843784:AAGzxOV6d7ZkxclNreC2yamuJHZordcoV8Q")

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Enter /find (verb)")

@bot.message_handler(commands=['find'])
def send_welcome(message):
	bot.send_message(message.chat.id, get_verbs(message.text.replace("/find ","")))
    

def json_load():
    with open("data.json","r") as f:
        return json.load(f)

def json_dump(data):
    with open("data.json","w") as f:
        json.dump(data,f)

def get_verbs(verb):
    
    data = json_load()
    try:
        print(f"[INFO] {data[verb.lower()]}")
    except:
        url = f"https://conjugator.reverso.net/conjugation-french-verb-{verb.lower()}.html"
        context = BeautifulSoup(requests.get(url).text,"lxml")
        verbs = []
        for txt in context.find_all('i',class_="verbtxt", limit=6):
            verbs.append(txt.get_text())
        data[verb.lower()] = {}
        data[verb.lower()] = {
            "verb": verb.lower(),
            "je":verbs[0],
            "tu":verbs[1],
            "il/elle":verbs[2],
            "nous":verbs[3],
            "vous":verbs[4],
            "ils/elles":verbs[5],
        }
        json_dump(data)
        print("[INFO] Use from parse")
        return f"Verb - {verb.lower()} \n\nJe - {verbs[0]} \nTu - {verbs[1]} \nIl/Elle - {verbs[2]} \nNous - {verbs[3]} \nVous - {verbs[4]} \nIls/Elles - {verbs[5]}"

        
    else:
        print("[INFO] Use from database")
        return f'Verb - {data[verb.lower()]["verb"]} \n\nJe - {data[verb.lower()]["je"]} \nTu - {data[verb.lower()]["je"]} \nIl/Elle - {data[verb.lower()]["je"]} \nNous - {data[verb.lower()]["je"]} \nVous - {data[verb.lower()]["je"]} \nIls/Elles - {data[verb.lower()]["je"]}'



bot.infinity_polling()