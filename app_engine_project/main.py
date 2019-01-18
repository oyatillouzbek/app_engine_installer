#!/usr/bin/env python
#-*-coding:utf8;-*-

project_name = "project_nomi" 
import fileworker as fv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import logging
import threading
import requests
import json
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import time
from time import *
from datetime import datetime, timedelta
import telebot
from telebot import types
import os
import random
import webapp2
import urllib
import urllib2
API_TOKEN = "replace_me_with_token"

def admin(user_id):
    Admins = [164135965] #Adminlar id si ro'yhati. Bu yerga o'zingizni id raqamingizni yozing. Tel raqam emas, telegramdagi id raqam
    return user_id in Admins

bot = telebot.TeleBot(API_TOKEN, threaded=False)
bot_id = int(API_TOKEN.split(":")[0])
webhook_key = (API_TOKEN.split(":")[1])[:-20]

def _print(a):
    logging.info(str(a))
    return

def get_date():
    return (datetime.now() + timedelta(hours=5)).strftime('%Y-%m-%d')

def get_datetime():
    return (datetime.now() + timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S')

def md(txt):
    return(txt.replace("_","\_").replace("*","\*").replace("`","\`").replace("[","\["))

@bot.channel_post_handler(func=lambda message: True, content_types=['text', 'photo','sticker','document','video','audio','voice'])
def channel_post(message):
    chat_id = message.chat.id
    text = str(message.text).decode("utf-8")
    if message.text == "soat+" or text == "soat":
        count = bot.get_chat_members_count(chat_id)
        kun=(datetime.now() + timedelta(hours=5)).strftime('%Y-%m-%d')
        soat=(datetime.now() + timedelta(hours=5)).strftime('%H:%M')
        if int(count) > 100:
            des=fv.open('./description.txt', 'r').read()
            if not str(chat_id) in des:
                fv.open('./description.txt', 'a').write(str(chat_id) + '\n')
                bot.delete_message(chat_id=chat_id, message_id=message.message_id)
                bio=bot.get_chat(chat_id).description
                bot.set_chat_description(chat_id, "📆 {0} ⏰{1}\n\n{2}".format(str(kun),str(soat),str(bio)))
                v=bot.send_message(chat_id, 'Soat funksiyasi faollashtirildi')
            else:
                m=bot.send_message(chat_id, 'Siz allaqachon soat funksiyasini faollashtirgansiz')
                bot.delete_message(chat_id=chat_id, message_id=m.message_id)
        else:
            bio=bot.get_chat(chat_id).description
            bot.set_chat_description(chat_id, "📆 {0} ⏰{1}\n\nBot 5K dan katta guruh va kanllarda ishlaydi\n{2}".format(str(kun),str(soat),str(bio)))
    elif message.text == "soat-":
        bot.delete_message(chat_id=chat_id, message_id=message.message_id)
        m=bot.send_message(chat_id, "Soat funksiyasini o'chirishni maslahat bermaymiz")
        bot.delete_message(chat_id=chat_id, message_id=m.message_id)
    else:
        'el'
        soatlar()

def soatlar():
    now=(datetime.now() + timedelta(hours=5)).strftime('%M')
    q=fv.open('./vaqt.txt', 'r').read()
    if not str(q) == str(now):
        fv.open('./vaqt.txt', 'w').write(str(now))
        des=fv.open('./description.txt', 'r').read()
        lis=[]
        lis.append(des)
        li=str(lis).replace("']","").replace("['","")
        for i in str(li).split('n'):#des.split('\n')
            try:
                kun=(datetime.now() + timedelta(hours=5)).strftime('%Y-%m-%d')
                soat=(datetime.now() + timedelta(hours=5)).strftime('%H:%M')
                bio=bot.get_chat(i[0:-1]).description
                bot.set_chat_description(i[0:-1], "📆 {0} ⏰{1}{2}".format(str(kun),str(soat),str(bio.replace(bio.split('\n')[0],''))))
            except:
                'ex'
    return

@bot.message_handler(func=lambda message: True)
def main(message):
    first_name = message.from_user.first_name.decode("utf-8") #hat yozgan odam ismi
    user_id = message.from_user.id #hat yozgan odam id si
    chat_id = message.chat.id #chat id si. Agar gruppa bo'sa chat_id<0, agar lichka bo'sa user_id bilan bir xil
    text = str(message.text).decode("utf-8") #yozilfan gat matni
    fv.open('./description.txt', 'w').write('\n')
    if len(text)>0: #agar text uzunligi 0 dan kotta bo'sa (hatolarni oldini olish uchun
        try:
            if chat_id>0: #lichka bo'sa
                if text == "/start":
                    bot.send_message(chat_id, "Bot ni kanal yoki guruhingizga admin qiling va kanal yoki guruhga soat+ yozing\n\nBot muallifi @bots_uz jamoasi")
                    try:
                        fv.open('./description.txt', 'r').read()
                    except:
                        fv.open('./description.txt', 'w').write('\n')
                        fv.open('./vaqt.txt', 'w').write('00')
                soatlar()
            else: #gruppa bo'sa
                if message.text == "soat+" or text == "soat" and bot.get_chat_member(chat_id, user_id).status in ("creator"):
                    count = bot.get_chat_members_count(chat_id)
                    if int(count) > 100:
                        des=fv.open('./description.txt', 'r').read()
                        if not str(chat_id) in des:
                            fv.open('./description.txt', 'a').write(str(chat_id) + '\n')
                            bot.delete_message(chat_id=chat_id, message_id=message.message_id)
                            kun=(datetime.now() + timedelta(hours=5)).strftime('%Y-%m-%d')
                            soat=(datetime.now() + timedelta(hours=5)).strftime('%H:%M')
                            bio=bot.get_chat(chat_id).description
                            bot.set_chat_description(chat_id, "📆 {0} ⏰{1}\n\n{2}".format(str(kun),str(soat),str(bio)))
                            v=bot.send_message(chat_id, 'Soat funksiyasi faollashtirildi')
                        else:
                            m=bot.send_message(chat_id, 'Siz allaqachon soat funksiyasini faollashtirgansiz')
                            bot.delete_message(chat_id=chat_id, message_id=m.message_id)
                    else:
                        bio=bot.get_chat(chat_id).description
                        bot.set_chat_description(chat_id, "📆 {0} ⏰{1}\n\nBot 5K dan katta guruh va kanllarda ishlaydi\n{2}".format(str(kun),str(soat),str(bio)))
                elif message.text == "soat-":
                    bot.delete_message(chat_id=chat_id, message_id=message.message_id)
                    m=bot.send_message(chat_id, "Soat funksiyasini o'chirishni maslahat bermaymiz")
                    bot.delete_message(chat_id=chat_id, message_id=m.message_id)
                else:
                    'el'
                    soatlar()
        except:
            'e'
    soatlar()    
    return


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

# webserver index
class IndexHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("""<!DOCTYPE html>
<html lang="uz">
  <head>
    <meta charset="utf-8">
    <title>""" + project_name + """</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content=""" + project_name + """ " ning serveri">
    <meta name="author" content="UzStudio">
    <link rel="shortcut icon" href="/favicon.ico">
  </head>
  <body>
    <h1><a href="tg:reslove?domain=uzstudio">""" + project_name + """</a> ning serveri</h1>
  </body>
</html>""")
        return


# bu joyiga teymela!!! Eng optimal qilip yozib bo'lingan!
# Process webhook calls
class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(600)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        try:
            json_string = json.loads(self.request.body.decode("utf-8"))
            updates = [telebot.types.Update.de_json(json_string)]
            new_messages = []
            edited_new_messages = []
            new_channel_posts = []
            new_edited_channel_posts = []
            new_inline_querys = []
            new_chosen_inline_results = []
            new_callback_querys = []
            for update in updates:
                if update.message:
                    new_messages.append(update.message)
                if update.edited_message:
                    edited_new_messages.append(update.edited_message)
                if update.channel_post:
                    new_channel_posts.append(update.channel_post)
                if update.edited_channel_post:
                    new_edited_channel_posts.append(update.edited_channel_post)
                if update.inline_query:
                    new_inline_querys.append(update.inline_query)
                if update.chosen_inline_result:
                    new_chosen_inline_results.append(update.chosen_inline_result)
                if update.callback_query:
                    new_callback_querys.append(update.callback_query)
            logger.debug('Received {0} new updates'.format(len(updates)))
            if len(new_messages) > 0:
                bot.process_new_messages(new_messages)
            if len(edited_new_messages) > 0:
                bot.process_new_edited_messages(edited_new_messages)
            if len(new_channel_posts) > 0:
                bot.process_new_channel_posts(new_channel_posts)
            if len(new_edited_channel_posts) > 0:
                bot.process_new_edited_channel_posts(new_edited_channel_posts)
            if len(new_inline_querys) > 0:
                bot.process_new_inline_query(new_inline_querys)
            if len(new_chosen_inline_results) > 0:
                bot.process_new_chosen_inline_query(new_chosen_inline_results)
            if len(new_callback_querys) > 0:
                bot.process_new_callback_query(new_callback_querys)    
        except Exception as ex:
            logging.error(str(ex))
        self.response.write('{"ok": true}')
        return

class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get("url")
        token = self.request.get("token")
        try:
            fv.open("./enabled_list.uzsdb","r").read()
        except:
            fv.open('./enabled_list.uzsdb',"w").write("0")

        try:
            fv.open("./history.uzsdb","r").read()
        except:
            fv.open('./history.uzsdb',"w").write("0")

        if not url:
            bot.set_webhook("https://" + project_name + ".appspot.com/" + webhook_key)
        elif token == API_TOKEN:
            bot.set_webhook(url)
        else:
            self.response.write("token noto'g'ri")
            return
        self.response.write("ok")
        return

app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/' + webhook_key, WebhookHandler),
], debug=True)
