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
    return (txt.replace("_", "\_").replace("*", "\*").replace("`", "\`").replace("[", "\["))


def getEnabled(chatid):
    try:
        fv.open('./enabled_list.uzsdb', 'r').read().split('\n').index(str(chatid))
        return True
    except:
        return False


def setEnabled(chatid, enable=True):
    enable_list = fv.open('./enabled_list.uzsdb', 'r').read().split('\n')
    if enable:
        enable_list.append(str(chatid))
    else:
        try:
            enable_list.remove(str(chatid))
        except:
            'ok'
    fv.open('./enabled_list.uzsdb', 'w').write('\n'.join(enable_list))
    return


@bot.inline_handler(lambda query: len(query.query.split()))
def qq(q):
    user_id = q.from_user.id
    meva = q.query
    spo = types.InlineKeyboardMarkup()
    tin = types.InlineKeyboardButton
    if "|" in meva:
        if meva.startswith('p'):
            pho = meva.split('|')[1]
            mpiarraqami = meva.split("|")[3]
            question = fv.open('./test/' + str(mpiarraqami) + '/question.txt', 'r').read()
            matn1 = str(question.split("|")[1][1:]).split("\n")
            spo = types.InlineKeyboardMarkup()
            for datas in matn1:
                x = datas
                hala = tin(text="{0}".format(str(x)), callback_data="&{0}|{1}".format(str(x[0]), str(mpiarraqami)))
                spo.add(*[hala])
            # spo.add(tin(text="Ulashish", switch_inline_query="{0}|{1}".format(str(user_id), str(mpiarraqami))))
            results = []
            no = len(fv.open('./test/' + str(mpiarraqami) + '/no.txt', 'r').read().split('\n')) - 2
            yes = len(fv.open('./test/' + str(mpiarraqami) + '/yes.txt', 'r').read().split('\n')) - 2
            try:
                c = int(no + yes) / 100
                no1 = no // c
                yes1 = yes // c
                message_text = "To'g'ri javob berganlar ✅\n{0}%\n{1} ta\n\nNoto'g'ri javob berganlar ❌\n{2}%\n{3} ta\n\n{4}".format(
                    str(yes1), str(yes), str(no1), str(no), str(question.split("|")[0]))
            except:
                message_text = "To'g'ri javob berganlar ✅\n{0} ta\n\nNoto'g'ri javob berganlar ❌\n{1} ta\n\n{2}".format(
                    str(yes), str(no), str(question.split("|")[0]))
            exit = types.InlineQueryResultPhoto('1', photo_url=pho,
                                                thumb_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5SaZm940oPxsIcpjwWVDkLOT4uj2IEyRdi7xQR-6V7GBBCpvw',
                                                caption=message_text, reply_markup=spo)
            bot.answer_inline_query(q.id, [exit], cache_time=1)
        else:
            try:
                mpiarraqami = meva.split("|")[1]
                question = fv.open('./test/' + str(mpiarraqami) + '/question.txt', 'r').read()
                matn1 = str(question.split("|")[1][1:]).split("\n")
                spo = types.InlineKeyboardMarkup()
                for datas in matn1:
                    x = datas
                    hala = tin(text="{0}".format(str(x)), callback_data="{0}|{1}".format(str(x[0]), str(mpiarraqami)))
                    spo.add(*[hala])
                # spo.add(tin(text="Ulashish", switch_inline_query="{0}|{1}".format(str(user_id), str(mpiarraqami))))
                results = []
                no = fv.open('./test/' + str(mpiarraqami) + '/no.txt', 'r').read()
                yes = fv.open('./test/' + str(mpiarraqami) + '/yes.txt', 'r').read()
                single_msg = types.InlineQueryResultArticle(
                    id="1",
                    title="Postni yuborish",
                    description=str(question.split("|")[0]),
                    input_message_content=types.InputTextMessageContent(
                        message_text=yes + "\n\n" + no + "\n\n{0}".format(str(question.split("|")[0])),
                        parse_mode="Markdown"),
                    reply_markup=spo
                )
                results.append(single_msg)
                bot.answer_inline_query(q.id, results)
            except:
                cid = q.query.split("|")[0]
                if q.query.startswith(str(cid)):
                    matn = q.query.replace(str(cid) + "|", "")
                    file1 = fv.open('./test/' + str(cid) + '/' + str(matn) + '.txt', 'r').read()
                    matn = file1.split("^|^")[0]
                    file = file1.split("\n")
                    spo = types.InlineKeyboardMarkup()
                    for x in file:
                        if x:
                            try:
                                data = x.replace(str(matn) + "^|^", "")
                            except:
                                data = x
                            sarlavha = data.split(" + ")[0]
                            link = data.split(" + ")[1]
                            try:
                                if link.startswith("https://t.me/"):
                                    mid = link.replace("https://t.me/", "@")
                                    count = bot.get_chat_members_count(mid)
                                    sarlavha = str(sarlavha) + " - " + str(count)
                            except:
                                link = link
                            hala = tin(text="{0}".format(str(sarlavha)), url="{0}".format(str(link)))
                            spo.add(*[hala])
                    spo.add(tin(text="Ulashish",
                                switch_inline_query="{0}|{1}".format(str(cid), str(q.query.split("|")[1]))))
                    results = []
                    single_msg = types.InlineQueryResultArticle(
                        id="1",
                        title="Postni yuborish",
                        description="Postni yuborish uchun shu yerga bosing",
                        input_message_content=types.InputTextMessageContent(message_text=str(matn)),
                        reply_markup=spo
                    )
                    results.append(single_msg)
                    bot.answer_inline_query(q.id, results)

    if "{0}|{1}\n".format(str(user_id), str(meva)) in fv.open('./test/2.txt', "r").read():
        matn = dec(fv.open('./test/{0}b.txt'.format(meva), 'r').read())
        key = fv.open('./test/{0}.txt'.format(meva), 'r').read()
        results = []
        single_msg = types.InlineQueryResultArticle(
            id="1",
            title="{0} - savol".format(str(meva)),
            description="Reytingni e'lon qilish",
            input_message_content=types.InputTextMessageContent(
                message_text="{0}\n\n*To'g'ri javoblari:*\n`{1}|{2}`\n\n*Barcha qatnashchilarga tashakkur!*".format(
                    str(matn), str(meva), str(key)), parse_mode="Markdown", disable_web_page_preview=True)
        )
        results.append(single_msg)
        bot.answer_inline_query(q.id, results)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    tin = types.InlineKeyboardButton
    user_id = call.from_user.id
    first_name = call.from_user.first_name.decode("utf-8")
    if call.inline_message_id:
        mpiarraqami = call.data.split("|")[1]
        exit = fv.open('./test/' + str(mpiarraqami) + '/exit.txt', 'r').read().split("\n")
        if exit.count(str(user_id)) == 0:
            fv.open('./test/' + str(mpiarraqami) + '/exit.txt', 'a').write(str(user_id) + "\n")
            question = fv.open('./test/' + str(mpiarraqami) + '/question.txt', 'r').read()
            dat = question.split("|")[-5][0] + "|" + mpiarraqami
            quest = str(question.split("|")[0])
            '''if call.data.startswith("&"):
                if call.data == '&' + str(question.split("|")[2][0]) + "|" + str(mpiarraqami):
                    fv.open('./test/' + str(mpiarraqami) + '/yes.txt', 'a').write(str(user_id) + '\n')
                    yes=fv.open('./test/' + str(mpiarraqami) + '/yes.txt', 'r').read()
                    matn1=str(question.split("|")[1][1:]).split("\n")
                    spo = types.InlineKeyboardMarkup()
                    for datas in matn1:
                        x=datas
                        hala=tin(text="{0}".format(str(x)), callback_data="&{0}|{1}".format(str(x[0]), str(mpiarraqami)))
                        spo.add(*[hala])
                    #spo.add(tin(text="Ulashish", switch_inline_query="{0}|{1}".format(str(user_id), str(mpiarraqami))))
                    no=len(fv.open('./test/' + str(mpiarraqami) + '/no.txt', 'r').read().split('\n'))-2
                    yes=len(fv.open('./test/' + str(mpiarraqami) + '/yes.txt', 'r').read().split('\n'))-2
                    try:
                        c=int(no+yes)/100
                        no1=no//c
                        yes1=yes//c
                        message_text = "To'g'ri javob berganlar ✅\n{0}%\n{1} ta\n\nNoto'g'ri javob berganlar ❌\n{2}%\n{3} ta\n\n{4}".format(str(yes1),str(yes),str(no1),str(no),str(question.split("|")[0]))
                    except:
                        message_text = "To'g'ri javob berganlar ✅\n{0} ta\n\nNoto'g'ri javob berganlar ❌\n{1} ta\n\n{2}".format(str(yes),str(no),str(question.split("|")[0]))
                    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = message_text, reply_markup=spo)
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=first_name + " siz to'g'ri javobni topdingiz ✅")
                else:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=first_name + " siz to'g'ri javobni topolmadingiz ❌")
                    fv.open('./test/' + str(mpiarraqami) + '/no.txt', 'a').write(str(user_id))
                    no=fv.open('./test/' + str(mpiarraqami) + '/no.txt', 'r').read()
                    matn1=str(question.split("|")[1][1:]).split("\n")
                    tin=types.InlineKeyboardButton
                    spo = types.InlineKeyboardMarkup()
                    for datas in matn1:
                        x=datas
                        hala=tin(text="{0}".format(str(x)), callback_data="&{0}|{1}".format(str(x[0]), str(mpiarraqami)))
                        spo.add(*[hala])
                    #spo.add(tin(text="Ulashish", switch_inline_query="{0}|{1}".format(str(user_id), str(mpiarraqami))))
                    no=len(fv.open('./test/' + str(mpiarraqami) + '/no.txt', 'r').read().split('\n'))-2
                    yes=len(fv.open('./test/' + str(mpiarraqami) + '/yes.txt', 'r').read().split('\n'))-2
                    try:
                        c=int(no+yes)/100
                        no1=no//c
                        yes1=yes//c
                        message_text = "To'g'ri javob berganlar ✅\n{0}%\n{1} ta\n\nNoto'g'ri javob berganlar ❌\n{2}%\n{3} ta\n\n{4}".format(str(yes1),str(yes),str(no1),str(no),str(question.split("|")[0]))
                    except:
                        message_text = "To'g'ri javob berganlar ✅\n{0} ta\n\nNoto'g'ri javob berganlar ❌\n{1} ta\n\n{2}".format(str(yes),str(no),str(question.split("|")[0]))
                    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = message_text, reply_markup=spo)'''
            if call.data == dat:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text=first_name + " siz to'g'ri javobni topdingiz ✅")
                fv.open('./test/' + str(mpiarraqami) + '/yes.txt', 'a').write(
                    "[{0}](tg://user?id={1}),".format(str(user_id), str(user_id)))
                no = fv.open('./test/' + str(mpiarraqami) + '/no.txt', 'r').read()
                yes = fv.open('./test/' + str(mpiarraqami) + '/yes.txt', 'r').read()
                matn1 = str(question.split("|")[1][1:]).split("\n")
                spo = types.InlineKeyboardMarkup()
                for datas in matn1:
                    x = datas
                    hala = tin(text="{0}".format(str(x)), callback_data="{0}|{1}".format(str(x[0]), str(mpiarraqami)))
                    spo.add(*[hala])
                # spo.add(tin(text="Ulashish", switch_inline_query="{0}|{1}".format(str(user_id), str(mpiarraqami))))
                bot.edit_message_text(inline_message_id=call.inline_message_id,
                                      text=yes + "\n\n" + no + "\n\n" + "{0}".format(quest), reply_markup=spo,
                                      parse_mode="Markdown", disable_web_page_preview=True)
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text=first_name + " siz to'g'ri javobni topolmadingiz ❌")
                fv.open('./test/' + str(mpiarraqami) + '/no.txt', 'a').write(
                    "[{0}](tg://user?id={1}),".format(str(user_id), str(user_id)))
                yes = fv.open('./test/' + str(mpiarraqami) + '/yes.txt', 'r').read()
                no = fv.open('./test/' + str(mpiarraqami) + '/no.txt', 'r').read()
                matn1 = str(question.split("|")[1][1:]).split("\n")
                tin = types.InlineKeyboardButton
                spo = types.InlineKeyboardMarkup()
                for datas in matn1:
                    x = datas
                    hala = tin(text="{0}".format(str(x)), callback_data="{0}|{1}".format(str(x[0]), str(mpiarraqami)))
                    spo.add(*[hala])
                # spo.add(tin(text="Ulashish", switch_inline_query="{0}|{1}".format(str(user_id), str(mpiarraqami))))
                bot.edit_message_text(inline_message_id=call.inline_message_id,
                                      text=yes + "\n\n" + no + "\n\n" + "{0}".format(quest), reply_markup=spo,
                                      parse_mode="Markdown", disable_web_page_preview=True)
        else:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text=first_name + " siz allaqachon javob bergansiz")
    if call.message:
        chat_id = call.message.chat.id
        if call.data.startswith('ty'):
            javob = call.data.replace('ty', '')
            if "{0}|{1}\n".format(str(user_id), str(javob)) in fv.open('./test/1.txt', "r").read():
                try:
                    tex = fv.open('./test/{0}a.txt'.format(javob), 'r').read()
                    listlash = map(lambda x: x.split("^|^"), tex.split("\n")[:-1])
                    saralash = list(enumerate(sorted(listlash, key=lambda aj: int(aj[-1]), reverse=True), 1))
                    texi = str(saralash).replace(", ['", ' ').replace("', '", ' ').replace("']), (", '\n').replace(
                        ', [', '').replace('"', ' ').replace(", '", ' ')[2:-4]
                    fv.open('./test/{0}b.txt'.format(javob), 'w').write("{0}".format(str(texi)))
                    spo = types.InlineKeyboardMarkup()
                    spo.add(types.InlineKeyboardButton(text="Natijalarni yuborish️",
                                                       switch_inline_query="{0}".format(str(javob))))
                    bot.send_message(user_id, "Javoblar saralandi!", reply_markup=spo)
                    fv.open('./test/2.txt', "a").write("{0}|{1}\n".format(str(user_id), str(javob)))
                except Exception as ex:
                    bot.send_message(164135965, "sort: " + str(ex))

        if call.data.startswith('+|') or call.data.startswith('-|'):
            if call.data.startswith('+|'):
                cou = int(fv.open('./bigtest/user/{0}/1.txt'.format(str(user_id)), 'r').read())
                fv.open('./bigtest/user/{0}/yes.txt'.format(str(user_id)), 'a').write('+')
                cou2 = int(fv.open('./bigtest/user/{0}/2.txt'.format(str(user_id)), 'r').read())
                mpiarraqami = call.data.split("|")[1]
                if cou == cou2 + 1:
                    ochko = int(len(fv.open('./bigtest/user/{0}/yes.txt'.format(str(user_id)), 'r').read()))
                    foiz = str(ochko * 100 / cou2)
                    bot.send_message(user_id, 'Savollarga ' + foiz + "% to'g'ri javob berdingiz")
                else:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text=first_name + " siz to'g'ri javobni topdingiz ✅")
                    question = fv.open('./bigtest/question/' + str(mpiarraqami) + '/question.txt', 'r').read()
                    a = question.split('#')
                    c = str(a[cou]).split('\n')
                    spo = types.InlineKeyboardMarkup()
                    matn0 = ''
                    for i in c:
                        # bot.send_message(user_id, i)
                        if i.startswith(' '):
                            matn0 = matn0 + "*{3}-savol: {0}\nMuallif:* [{1}](tg://user?id={2})".format(str(i[1:]),
                                                                                                        str(user_id),
                                                                                                        str(user_id),
                                                                                                        str(cou))
                        if i.startswith('- ') or i.startswith('+ '):
                            d = i[0]
                            e = i[2:]
                            hala = tin(text="{0}".format(str(e)),
                                       callback_data="{0}|{1}".format(str(d), str(mpiarraqami)))
                            spo.add(*[hala])
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="{0}\n`@sjt1bot {1}|{2}`".format(matn0, str(user_id),
                                                                                       str(mpiarraqami)),
                                          reply_markup=spo, parse_mode="Markdown")
                    fv.open('./bigtest/user/{0}/1.txt'.format(str(user_id)), 'w').write(str(cou + 1))
            if call.data.startswith('-|'):
                cou = int(fv.open('./bigtest/user/{0}/1.txt'.format(str(user_id)), 'r').read())
                cou2 = int(fv.open('./bigtest/user/{0}/2.txt'.format(str(user_id)), 'r').read())
                if cou == cou2 + 1:
                    ochko = int(len(fv.open('./bigtest/user/{0}/yes.txt'.format(str(user_id)), 'r').read()))
                    foiz = str(ochko * 100 / cou2)
                    bot.send_message(user_id, 'Savollarga ' + foiz + "% to'g'ri javob berdingiz")
                else:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text=first_name + " siz to'g'ri javobni topolmadingiz ❌")
                    mpiarraqami = call.data.split("|")[1]
                    question = fv.open('./bigtest/question/' + str(mpiarraqami) + '/question.txt', 'r').read()
                    a = question.split('#')
                    c = str(a[cou]).split('\n')
                    spo = types.InlineKeyboardMarkup()
                    matn0 = ''
                    for i in c:
                        if i.startswith(' '):
                            matn0 = matn0 + "*{3}-savol: {0}\nMuallif:* [{1}](tg://user?id={2})".format(str(i[1:]),
                                                                                                        str(user_id),
                                                                                                        str(user_id),
                                                                                                        str(cou))
                        if i.startswith('- ') or i.startswith('+ '):
                            d = i[0]
                            e = i[2:]
                            hala = tin(text="{0}".format(str(e)),
                                       callback_data="{0}|{1}".format(str(d), str(mpiarraqami)))
                            spo.add(*[hala])
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="{0}\n`@sjt1bot {1}|{2}`".format(matn0, str(user_id),
                                                                                       str(mpiarraqami)),
                                          reply_markup=spo, parse_mode="Markdown")
                    fv.open('./bigtest/user/{0}/1.txt'.format(str(user_id)), 'w').write(str(cou + 1))

        if fv.open('./test/' + str(call.data.split("|")[1]) + '/exit.txt', 'r').read().split("\n").count(
                str(user_id)) == 0:
            mpiarraqami = call.data.split("|")[1]
            fv.open('./test/' + str(mpiarraqami) + '/exit.txt', 'a').write(str(user_id) + "\n")
            question = fv.open('./test/' + str(mpiarraqami) + '/question.txt', 'r').read()
            dat = question.split("|")[-5][0] + "|" + mpiarraqami
            '''if call.data.startswith("&"):
                if call.data == '&' + str(question.split("|")[2][0]) + "|" + str(mpiarraqami):
                    fv.open('./test/' + str(mpiarraqami) + '/yes.txt', 'a').write(str(user_id))
                    yes=fv.open('./test/' + str(mpiarraqami) + '/yes.txt', 'r').read()
                    matn1=str(question.split("|")[1][1:]).split("\n")
                    spo = types.InlineKeyboardMarkup()
                    for datas in matn1:
                        x=datas
                        hala=tin(text="{0}".format(str(x)), callback_data="&{0}|{1}".format(str(x[0]), str(mpiarraqami)))
                        spo.add(*[hala])
                    #spo.add(tin(text="Ulashish", switch_inline_query="{0}|{1}".format(str(user_id), str(mpiarraqami))))
                    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = yes + "\n\n{0}`{1}`".format(call.message.caption.split("@sjt1bot")[0],"@sjt1bot" + call.message.caption.split("@sjt1bot")[1]), reply_markup=spo)
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=first_name + " siz to'g'ri javobni topdingiz ✅")
                else:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=first_name + " siz to'g'ri javobni topolmadingiz ❌")
                    fv.open('./test/' + str(mpiarraqami) + '/no.txt', 'a').write(str(user_id))
                    no=fv.open('./test/' + str(mpiarraqami) + '/no.txt', 'r').read()
                    matn1=str(question.split("|")[1][1:]).split("\n")
                    tin=types.InlineKeyboardButton
                    spo = types.InlineKeyboardMarkup()
                    for datas in matn1:
                        x=datas
                        hala=tin(text="{0}".format(str(x)), callback_data="&{0}|{1}".format(str(x[0]), str(mpiarraqami)))
                        spo.add(*[hala])
                    #spo.add(tin(text="Ulashish", switch_inline_query="{0}|{1}".format(str(user_id), str(mpiarraqami))))
                    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = no + "\n\n{0}`{1}`".format(call.message.caption.split("@sjt1bot")[0],"@sjt1bot" + call.message.caption.split("@sjt1bot")[1]), reply_markup=spo)'''
            if call.data == dat:
                fv.open('./test/' + str(mpiarraqami) + '/yes.txt', 'a').write(
                    "[{0}](tg://user?id={1}),".format(str(user_id), str(user_id)))
                yes = fv.open('./test/' + str(mpiarraqami) + '/yes.txt', 'r').read()
                matn1 = str(question.split("|")[1][1:]).split("\n")
                spo = types.InlineKeyboardMarkup()
                for datas in matn1:
                    x = datas
                    hala = tin(text="{0}".format(str(x)), callback_data="{0}|{1}".format(str(x[0]), str(mpiarraqami)))
                    spo.add(*[hala])
                # spo.add(tin(text="Ulashish", switch_inline_query="{0}|{1}".format(str(user_id), str(mpiarraqami))))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=yes + "\n\n{0}`{1}`".format(call.message.text.split("@sjt1bot")[0],
                                                                       "@sjt1bot" +
                                                                       call.message.text.split("@sjt1bot")[1]),
                                      reply_markup=spo, parse_mode="Markdown", disable_web_page_preview=True)
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text=first_name + " siz to'g'ri javobni topdingiz ✅")
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text=first_name + " siz to'g'ri javobni topolmadingiz ❌")
                fv.open('./test/' + str(mpiarraqami) + '/no.txt', 'a').write(
                    "[{0}](tg://user?id={1}),".format(str(user_id), str(user_id)))
                no = fv.open('./test/' + str(mpiarraqami) + '/no.txt', 'r').read()
                matn1 = str(question.split("|")[1][1:]).split("\n")
                tin = types.InlineKeyboardButton
                spo = types.InlineKeyboardMarkup()
                for datas in matn1:
                    x = datas
                    hala = tin(text="{0}".format(str(x)), callback_data="{0}|{1}".format(str(x[0]), str(mpiarraqami)))
                    spo.add(*[hala])
                # spo.add(tin(text="Ulashish", switch_inline_query="{0}|{1}".format(str(user_id), str(mpiarraqami))))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=no + "\n\n{0}`{1}`".format(call.message.text.split("@sjt1bot")[0],
                                                                      "@sjt1bot" +
                                                                      call.message.text.split("@sjt1bot")[1]),
                                      reply_markup=spo, parse_mode="Markdown", disable_web_page_preview=True)

        else:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text=first_name + " siz allaqachon javob bergansiz")


def dec(xitoy2):
    cr = ['xd0x90', 'xd0xb0', 'xd0x91', 'xd0xb1', 'xd0x92', 'xd0xb2', 'xd0x93', 'xd0xb3', 'xd0x94', 'xd0xb4', 'xd0x95',
          'xd0xb5', 'xd0x81', 'xd1x91', 'xd0x96', 'xd0xb6', 'xd0x97', 'xd0xb7', 'xd0x98', 'xd0xb8', 'xd0x99', 'xd0xb9',
          'xd0x9a', 'xd0xba', 'xd0x9b', 'xd0xbb', 'xd0x9c', 'xd0xbc', 'xd0x9d', 'xd0xbd', 'xd0x9e', 'xd0xbe', 'xd0x9f',
          'xd0xbf', 'xd0xa0', 'xd1x80', 'xd0xa1', 'xd1x81', 'xd0xa2', 'xd1x82', 'xd0xa3', 'xd1x83', 'xd0xa4', 'xd1x84',
          'xd0xa5', 'xd1x85', 'xd0xa6', 'xd1x86', 'xd0xa7', 'xd1x87', 'xd0xa8', 'xd1x88', 'xd0xa9', 'xd1x89', 'xd0xaa',
          'xd1x8a', 'xd0xab', 'xd1x8b', 'xd0xac', 'xd1x8c', 'xd0xad', 'xd1x8d', 'xd0xae', 'xd1x8e', 'xd0xaf', 'xd1x8f',
          'xd2x9a', 'xd2x9b', 'xd2x92', 'xd2x93', 'xd0x8e', 'xd1x9e', 'xd2xb2', 'xd2xb3']
    la = ['А', 'а', 'Б', 'б', 'В', 'в', 'Г', 'г', 'Д', 'д', 'Е', 'е', 'Ё', 'ё', 'Ж', 'ж', 'З', 'з', 'И', 'и', 'Й', 'й',
          'К', 'к', 'Л', 'л', 'М', 'м', 'Н', 'н', 'О', 'о', 'П', 'п', 'Р', 'р', 'С', 'с', 'Т', 'т', 'У', 'у', 'Ф', 'ф',
          'Х', 'х', 'Ц', 'ц', 'Ч', 'ч', 'Ш', 'ш', 'Щ', 'щ', 'Ъ', 'ъ', 'Ы', 'ы', 'Ь', 'ь', 'Э', 'э', 'Ю', 'ю', 'Я', 'я',
          'Қ', 'қ', 'Ғ', 'ғ', 'Ў', 'ў', 'Ҳ', 'ҳ']
    xitoy2 = xitoy2.replace("\\", '')
    for i in range(74):
        try:
            if cr[i] in xitoy2:
                xitoy2 = xitoy2.replace(cr[i], la[i])
        except:
            ' '
    return xitoy2


@bot.message_handler(func=lambda message: True,content_types=['text'])
def main(message):
    first_name = message.from_user.first_name.decode("utf-8")  # hat yozgan odam ismi
    user_id = message.from_user.id  # hat yozgan odam id si
    chat_id = message.chat.id  # chat id si. Agar gruppa bo'sa chat_id<0, agar lichka bo'sa user_id bilan bir xil
    username = message.chat.username
    text = str(message.text).decode("utf-8")  # yozilfan gat matni
    tin = types.InlineKeyboardButton
    if len(text) > 0 and chat_id < 0::  # agar text uzunligi 0 dan kotta bo'sa (hatolarni oldini olish uchun  and user_id == 164135965
        if text.endswith("]"):
            if text.startswith("[") and len(re.findall("[|]", text)) == 2:
                try:
                    mpiarraqami = fv.open('./test/0.txt', "r").read()
                    matn = text[1:-1]
                    matn0 = matn.split("|")[0]
                    ma = matn.replace(matn0, "")
                    matn0 = "*Savol: {0}\nMuallif:* [{1}](tg://user?id={2})".format(str(matn0), str(user_id),
                                                                                    str(user_id))
                    teks = str(matn0) + str(ma) + "|`@sjt1bot {0}|{1}`^||^".format(str(user_id),
                                                                                          str(mpiarraqami))
                    fv.open('./test/' + str(mpiarraqami) + '/question.txt', 'w').write(teks)
                    spo = types.InlineKeyboardMarkup()
                    matn1 = str(matn.split("|")[1][1:]).split("\n")
                    #                matn2=matn0 + "\n" + matn.split("|")[2]
                    for data in matn1:
                        x = data
                        if "|" in x:
                            x = x.split("|")[0]
                            hala = tin(text="{0}".format(str(x)),
                                       callback_data="{0}|{1}".format(str(x[0]), str(mpiarraqami)))
                            spo.add(*[hala])
                        else:
                            hala = tin(text="{0}".format(str(x)),
                                       callback_data="{0}|{1}".format(str(x[0]), str(mpiarraqami)))
                            spo.add(*[hala])
                    spo.add(
                        tin(text="Ulashish", switch_inline_query="{0}|{1}".format(str(user_id), str(mpiarraqami))))
                    bot.send_message(chat_id, text="{0}\n`@sjt1bot {1}|{2}`".format(matn0, str(user_id),
                                                                                           str(mpiarraqami)),
                                     reply_markup=spo, parse_mode="Markdown")
                    bot.send_message(164135965, text="{0}\n`@sjt1bot {1}|{2}`".format(matn0, str(user_id),
                                                                                             str(mpiarraqami)),
                                     reply_markup=spo, parse_mode="Markdown")
                    fv.open('./test/' + str(mpiarraqami) + '/yes.txt', 'w').write("To'g'ri javob berganlar ✅\n")
                    fv.open('./test/' + str(mpiarraqami) + '/no.txt', 'w').write("Noto'g'ri javob berganlar ❌\n")
                    fv.open('./test/' + str(mpiarraqami) + '/exit.txt', 'w').write("1\n")
                    mpiarraqami = int(mpiarraqami) + 1
                    fv.open('./test/0.txt', "w").write(str(mpiarraqami))
                except Exception as ex:
                    bot.send_message(chat_id, "Test no'to'g'ri yasalgan, qaytadan urinib ko'ring")
        if text.startswith("(") and text.endswith(")"):
            if '|' + str(text[1:-1]) in fv.open('./test/2.txt', "r").read():
                ff = fv.open('./test/{0}j.txt'.format(str(text[1:-1])), 'r').read()
                bot.send_chat_action(message.chat.id, 'typing')
                rr = re.findall(str(user_id) + ' Xato javoblar: [/[, \d\]]+', ff)
                bot.send_message(chat_id, rr)
            else:
                bot.send_message(chat_id,
                                 "Test yakunlanganidan keyin qaysi javoblarga xato javob berganingizni ko'rasiz.")
		if text.startswith("+"):
	        tex = text.lower()[1:]
	        post = open('./test/0.txt', "r").read()
	        if '1' in text:
	            for i in range(10):
	                tex = str(tex).replace(str(i), "")
	            open('./test/{0}.txt'.format(post), 'w').write(str(tex))
	            open('./test/1.txt', "a").write("{0}|{1}\n".format(str(user_id), str(post)))
	            open('./test/0.txt', "w").write(str(int(post) + 1))
	            bot.send_message(chat_id,
	                             "\U0001f4d6 Test nomeri: {0}\n\U0001f4e9 Foydalanuvchilar javobni quyidagi ko'rinishlarda botga yuborishsin.\n\n<code>{0}|{1}</code>\n\n<code>{0}/{1}</code> "
	                             "\n\n<code>{0},{1}</code>\n\n<code>{0}#{1}</code>\n\n<code>{0}*{1}</code>\n\n<code>{0}:{1}</code>\n\n<code>{0}@{1}</code>\n\nTestingizga kamida 2 kishi javob berganidan keyin <b>Testni yakunlash</b> tugmasini bosing.".format(
	                                 str(post), str(tex)), parse_mode="HTML")
	        else:
	            open('./test/{0}.txt'.format(post), 'w').write(str(tex))
	            open('./test/1.txt', "a").write("{0}|{1}\n".format(str(user_id), str(post)))
	            open('./test/0.txt', "w").write(str(int(post) + 1))
	            bot.send_message(chat_id,
	                             "\U0001f4d6 Test nomeri: {0}\n\U0001f4e9 Foydalanuvchilar javobni quyidagi ko'rinishlarda botga yuborishsin.\n\n<code>{0}|{1}</code>\n\n<code>{0}/{1}</code> "
	                             "\n\n<code>{0},{1}</code>\n\n<code>{0}#{1}</code>\n\n<code>{0}*{1}</code>\n\n<code>{0}:{1}</code>\n\n<code>{0}@{1}</code>\n\nTestingizga kamida 2 kishi javob berganidan keyin <b>Testni yakunlash</b> tugmasini bosing.".format(
	                                 str(post), str(tex)), parse_mode="HTML")
	    if text[0].isdigit():
	        if len(re.findall("\W+", text)) == 1 and not " " in text:
	            if first_name:
	                q = str(re.split(r'\W+', text)[0])
	                savol = []
	                if '|' + str(q) + '\n' in open('./test/1.txt', "r").read():
	                    try:
	                        open('./test/{0}a.txt'.format(q), 'r').read()
	                    except:
	                        open('./test/{0}a.txt'.format(q), 'w').write("")
	                    if str(user_id) in open('./test/{0}a.txt'.format(q), 'r').read():
	                        bot.send_message(chat_id, first_name + " siz allaqachon javob bergansiz")
	                    elif '\n' + str(q) + '\n' in open('./test/2.txt', "r").read():
	                        bot.send_message(chat_id, "Javob berish muddati tugagan")
	                    else:
	                        spo = types.InlineKeyboardMarkup()
	                        spo.add(types.InlineKeyboardButton(text="Testni yakunlash?",
	                                                           callback_data="ty{0}".format(str(q))))
	                        savo = open('./test/{0}.txt'.format(q), 'r').read()
	                        x = 0
	                        savol.append(savo)
	                        w1 = str(str(savol)[2:-2])
	                        w2 = str(re.split(r'\W+', text)[1]).lower()
	                        if '1' in text:
	                            for i in range(10):
	                                w2 = str(w2).replace(str(i), "")
	                        j = []
	                        #try:
	                        if len(w1) == len(w2) and not 105 == len(w2):
	                            e = []
	                            while True:
	                                if len(w1) == int(x):
	                                    break
	                                if w1[x] != w2[x]:
	                                    j.append(x + 1)
	                                    e.append(x + 1)
	                                x += 1
	                            javob = """\U0001f464 Foydalanuvchi ismi: <a href="tg://user?id={4}">{3}</a> <code>{3}</code>\n\U0001f4d6 Test nomeri: {0}\n\u270f\ufe0f Jami savollar soni: {1} ta\n\u2705 To'g'ri javoblar soni: {2} ta\n\U0001f550{5}""".format(
	                                str(q), str(len(w1)), str(len(w1) - len(e)), str(first_name),
	                                str(user_id), str(get_datetime()))
	                            open('./test/{0}a.txt'.format(q), 'a').write(
	                                "[{0}](tg://user?id={1})^|^{2}\n".format(str(first_name[0:10]),
	                                                                         str(user_id),
	                                                                         str(len(w1) - len(e))))
	                            bot.send_message(164135965, str(javob), parse_mode="HTML")
	                            bot.send_message(chat_id, str(javob), parse_mode="HTML")
	                            open('./test/{0}j.txt'.format(q), 'a').write(
	                                str(user_id) + ' Xato javoblar: ' + str(j) + '\n')
	                            bot.send_message(chat_id, "Javoblaringiz qabul qilindi")
	                            ids = open('./test/1.txt', "r").read()
	                            cid = str(re.findall("[0-9]+[|]" + str(q), ids)).split('|')
	                            bot.send_message(cid[0][2:],
	                                             '<a href="tg://user?id={1}">{0}</a> {2}-testning javoblarini yubordi'.format(
	                                                 str(first_name), str(user_id), str(cid[1][:-2])),
	                                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Testni yakunlash?",callback_data="ty{0}".format(str(q)))]]), parse_mode="HTML")
	                        if 105 == len(w2):
	                            e = []
	                            while True:
	                                if len(w1) == int(x):
	                                    break
	                                if x < 45:
	                                    if w1[x] != w2[x]:
	                                        e.append(2.1)
	                                        j.append(x + 1)
	                                    x += 1
	                                if x > 44 and 106 > x:
	                                    if w1[x] != w2[x]:
	                                        e.append(3.1)
	                                        j.append(x + 1)
	                                    x += 1
	                            javob = """?\U0001f464 Foydalanuvchi ismi: <a href="tg://user?id={4}">{3}</a> <code>{3}</code>\n?\U0001f4d6 Test nomeri: {0}\n\u270f\ufe0f Jami savollar soni: {1} ta\n\u2705 To'plagan balingiz:  {2}\n? {5}""".format(
	                                str(q), str(len(w1)), str(280.5 - sum(e)), str(first_name), str(user_id),
	                                str(get_datetime()))
	                            open('./test/{0}a.txt'.format(q), 'a').write("[{0}](tg://user?id={1})^|^{2}\n".format(str(first_name[0:10]),str(user_id), str(280.5 - int(str(sum(e)).split('.')[0]))))
	                            bot.send_message(164135965, str(javob), parse_mode="HTML")
	                            open('./test/{0}j.txt'.format(q), 'a').write(
	                                str(user_id) + ' Xato javoblar: ' + str(j) + '\n')  # faqat blok test un
	                            bot.send_message(chat_id, str(javob), parse_mode="HTML")
	                            bot.send_message(chat_id, "Javoblaringiz qabul qilindi")
	                            ids = open('./test/1.txt', "r").read()
	                            cid = str(re.findall("[0-9]+[|]" + str(q), ids)).split('|')
	                            bot.send_message(cid[0][2:],
	                                             '<a href="tg://user?id={1}">{0}</a> {2}-testning javoblarini yubordi'.format(
	                                                 str(first_name), str(user_id), str(cid[1][:-2])),
	                                             reply_markup=spo, parse_mode="HTML")
	                        if not len(w1) == len(w2):
	                            bot.send_message(chat_id, str(q) + "-testda savollar soni " + str(
	                                len(w1)) + " ta\nSiz esa " + str(len(w2)) + " ta javob yozdingiz.")
	                        #except Exception as ex:
	                            #pass
	                            #bot.send_message(chat_id, str(ex))
	                else:
	                    bot.send_message(chat_id, "Bunday test nomeri mavjud emas")
	            else:
	                bot.send_message(chat_id, str(
	                    first_name) + " bu nikingiz testga qbul qilinmadi.Nikingizni faqat lotin harflarida yozing")
	        else:
	            bot.send_message(chat_id, "Javoblarni mana shu tartibda yozing\n1996|abccbddaa")
        if text == '/nanyang':
            bot.send_message(164135965, 'xenan')
            open('./test/0.txt', 'w').write('1')
            open('./test/2.txt', 'w').write('0|0')
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
