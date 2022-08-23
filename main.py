#project - Parser_FR_words , Author - Maksymenko Kyrylo


import os
import time
from ast import Pass
from itertools import count
import requests
import json
from bs4 import BeautifulSoup
import telebot

bot = telebot.TeleBot("5299843784:AAGzxOV6d7ZkxclNreC2yamuJHZordcoV8Q")

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Enter (verb)")   

@bot.message_handler(commands=['trad'])
def translate_verb(message):
    trad_verb = message.text.replace("/trad ","")

    txt,path_ogg = traduit_verb(trad_verb)
    bot.send_message(message.chat.id, txt)
    bot.send_voice(message.chat.id, open(path_ogg, 'rb'))
    os.remove(path_ogg) 
    

@bot.message_handler(func=lambda message: True)
def find_verb(message):
    if message.text not in ["Present","Imparfait","Futur","Passe simple","Passe compose","Plus-que-parfait","Passe anterieur","Futur anterieur","Traduit"]:
        markup = types.ReplyKeyboardMarkup()
        itemPresent = types.KeyboardButton('Present')
        itemImparfait = types.KeyboardButton('Imparfait')
        itemFutur = types.KeyboardButton('Futur')
        itemPasseSimple = types.KeyboardButton('Passe compose')
        itemTrad = types.KeyboardButton('Traduit')
        
        markup.row(itemPresent, itemImparfait)
        markup.row(itemFutur, itemPasseSimple)
        markup.row(itemTrad)
        data = json_load()
        try:
            print(data["users_history"][message.chat.id])
        except:
            data["users_history"][message.chat.id]= ""
        data["users_history"][message.chat.id]= (message.text).lower()  #.replace("/find ","")
        json_dump(data)
        bot.send_message(message.chat.id, "Choose one time:", reply_markup=markup)
        return 

    data = json_load()
    last_verb = data["users_history"][str(message.chat.id)]
    
    if message.text in ["Present","Imparfait","Futur","Passe simple","Passe compose","Plus-que-parfait","Passe anterieur","Futur anterieur","Traduit"]:
        if message.text == "Traduit":
            txt,path_ogg = traduit_verb(last_verb)
            bot.send_message(message.chat.id, txt)
            bot.send_voice(message.chat.id, open(path_ogg, 'rb'))
            os.remove(path_ogg) 
            return
        print(f"a {last_verb}")
        get_verbs(last_verb,message.text)
        data = json_load()
        bot.send_message(message.chat.id, make_text(data,message.text,last_verb))
        return

def json_load():
    with open("data.json","r") as f:
        return json.load(f)

def json_dump(data):
    with open("data.json","w") as f:
        json.dump(data,f)

def make_text_trad(fm_tr,tr_lg,tr_vb,tr,trad_lg_tld):
    print("[INFO] Create text Traduction")
    txt_start = "-------Traduction-------"
    txt_lang = f"   From - {fm_tr.upper()} To - {tr_lg.upper()}"
    txt_trad = f"     {tr_vb} -> {tr}"
    txt_end = "-------------------------------"
    txt = f"{txt_start}\n{txt_lang}\n\n{txt_trad}\n{txt_end}"

    tts = gTTS(tr, lang=tr_lg, tld=trad_lg_tld)
    tts.save(f'source\{tr}.ogg')
    
    print(txt)
    return txt,f'source\{tr}.ogg'

def make_text(data, time, verb):
    print("[INFO] Create text Conjugaison")
    txt_start = "-------Conjugaison-------"
    txt_name= f"    Verb - {verb}"
    txt_verbs = ""
    for key,item in data["data_verbs"][verb][time].items():
        txt_verbs = f"{txt_verbs}\n     {key} - {item}"
    txt_end = "----------------------------------"
    txt = f"{txt_start}\n{txt_name}\n{txt_verbs}\n{txt_end}"
    print(txt)
    return txt,

def traduit_verb(verb):
    support_lang = ["uk","fr","ru","en"]
    if translator.detect(verb).lang == "fr" or translator.detect(verb).lang == "en":
        print("France")
        trad = translator.translate(verb, src="fr", dest='uk').text
        from_trad = "fr"
        trad_lg = "uk"
        trad_lg_tld = "com"
    if translator.detect(verb).lang == "uk" or translator.detect(verb).lang == "ru":
        print("Ukrain")
        trad = translator.translate(verb, src="uk", dest='fr').text
        from_trad = translator.detect(verb).lang
        trad_lg = "fr"
        trad_lg_tld = "fr"
    if translator.detect(verb).lang not in support_lang:
        error = "Je ne comprends pas / я не розумію\n[ERROR] Language not support" 
        print("[ERROR] Language not support")
        return error
    return make_text_trad(from_trad,trad_lg,verb,trad,trad_lg_tld)

def get_verbs(verb, tm):
    
    data = json_load()
    try:
        print(f'[INFO] {data["data_verbs"][verb.lower()]}')
    except:
        url = f"https://conjugator.reverso.net/conjugation-french-verb-{verb.lower()}.html"
        context = BeautifulSoup(requests.get(url).text,"lxml")
        verbs = {}
        times = ["Present","Imparfait","Futur","Passe simple","Passe compose","Plus-que-parfait","Passe anterieur","Futur anterieur"]
        i = 0
        for tm in context.find_all("ul",class_="wrap-verbs-listing",limit=8):
            verbs[times[i]] = []
            for txt in tm.find_all("li"):
                if txt.get("v") != "2":
                    verbs[times[i]].append(txt.get_text())
            i = i + 1

        data["data_verbs"][verb.lower()] = {}

        for a in range(0,len(times)):
            data["data_verbs"][verb.lower()][times[a]] = {}
            print(times[a])
            list_obj = ["Je","Tu","Il","Elle","Nous","Vous","Ils","Elles","Il/Elle","Ils/Elles"]
            list_spec = ["je","tu","ils","elles","nous","vous","il","elles","il/elle","ils/elles","j'"]

            for item in verbs[times[a]]:
                
                print(f"[INFO] Item {item}")
                item_ls = item.replace("'"," ").split()
                obj = " ".join(item_ls[1:])
                pref = item_ls[0]
                if item_ls[0] == "j":
                    pref = "je"
                
                print(f"[INFO] Item transform  {obj}")

                data["data_verbs"][verb.lower()][times[a]].update({pref:obj})
                print(data["data_verbs"][verb.lower()][times[a]])
                
            print(f"[INFO] Eterarion {a + 1}/{len(times)}")

        
        json_dump(data)
        print("[INFO] Use from parse")
        
        return #make_text(data, tm, verb)
        
    else:
        print("[INFO] Use from database")
        return #make_text(data, tm, verb)


bot.infinity_polling()
