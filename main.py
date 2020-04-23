#!/usr/bin/python
#-*-coding:utf-8-*-
import os
import threading
from app_engine_project import requests
import json
import re
import sys
import time
try:
    reload(sys)
    sys.setdefaultencoding("utf-8")
except:
    'py3 uchun keremas'
    
def r_input(x):
    try:
        return(raw_input(str(x)))
    except:
        return(input(str(x)))
    
def a():
    data = requests.get("https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.70.zip").content
    open('./master.zip',"wb").write(data)
    del(data)
    os.system("unzip -qu master.zip")
    
def up(INPUT):
    requests.get("https://api.telegram.org/bot{}/deleteWebhook".format(INPUT.split(' ')[0])).text
    requests.get("https://api.telegram.org/bot{}/getUpdates?offset=-1".format(INPUT.split(' ')[0])).text
    requests.get("https://api.telegram.org/bot{}/setWebhook?url=https://{}.appspot.com/{}".format(INPUT.split(' ')[0], INPUT.split(' ')[1], (INPUT.split(' ')[0].split(":")[1])[:-20])).text
    
threading.Thread(target=a).start()
INPUT = r_input("TOKEN PROJECT_ID: ")
API_TOKEN=INPUT.split(' ')[0]
try:
    requests.get("https://api.telegram.org/bot", timeout=5).text
    data = requests.get("https://api.telegram.org/bot" + API_TOKEN + "/getMe", timeout = 10).text
    username = json.loads(data)["result"]['username']
    print("\n\nbotingiz topildi! username: @" + username)
except Exception as ex:
    print("Tokenda muammo\n"+str(ex))

project_id = INPUT.split(' ')[1]
data = open('app_engine_installer/app_engine_project/app.yaml','r').read()
data = data.replace('project_nomi', project_id)
open('app_engine_installer/app_engine_project/app.yaml','w').write(data)
data = open('app_engine_installer/app_engine_project/main.py','r').read().replace('project_nomi', project_id).replace('replace_me_with_token',API_TOKEN)
open('app_engine_installer/app_engine_project/main.py','w').write(data)
os.system('google_appengine/appcfg.py -A '+ project_id + " update app_engine_installer/app_engine_project/app.yaml --noauth_local_webserver")
try:
    requests.get('https://' + project_id + ".appspot.com/set_webhook").text
    #threading.Thread(target=up, args=(INPUT,)).start()
    up(INPUT)
    print("Agar siz hammasini to'g'ri qilgan bo'lsangiz, bo't ishga tushdi.")
except Exception as ex:
    print("Server ishlamiyopti. Qandaydir hato bo'lgan. Qaytadan harakat qilinmoqda...")
    os.system("google_appengine/appcfg.py set_default_version /app_engine_installer/app_engine_project --noauth_local_webserver")
    os.system('google_appengine/appcfg.py -A '+ project_id + " update app_engine_installer/app_engine_project/app.yaml --noauth_local_webserver")
open("./upload_" + project_id + ".sh",'w').write('google_appengine/appcfg.py -A '+ project_id + " update app_engine_installer/app_engine_project/app.yaml --noauth_local_webserver") 

