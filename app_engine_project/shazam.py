API_TOKEN=''
bot1=telebot.TeleBot(API_TOKEN, threaded=False)
try:
    def vka(text, i):
        import vk_api
        from vk_api.audio import VkAudio
        login, password = 'LOGIN', 'PASSWORD'#vk.com dagi login parolizi kiritasiz
        vk_session = vk_api.VkApi(login, password)
        try:
            vk_session.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)
        vkaudio = VkAudio(vk_session)
        lis=[]
        if i == 1:
            tracks = vkaudio.search(q=text, count=i)
            for track in tracks:
                title=track['title']
                artist=track['artist']
                url=track['url'].split('?')[0]
                lis=[str(title),str(artist), url]
                if lis:
                    break
        else:
            group=[]
            tracks = vkaudio.search(q=text)
            for track in tracks:
                title=track['title']
                artist=track['artist']
                url=track['url'].split('?')[0]
                group=[str(artist), str(title), url]
                lis.append(group)
        return lis

    @bot1.inline_handler(lambda query: len(query.query.split()))
    def qq(q):
        try:
            chat_id = q.from_user.id
            mp3 = str(q.query)
            spo = types.InlineKeyboardMarkup()
            tin=types.InlineKeyboardButton
            results = []
            import uuid
            if len(str(mp3)) > 2:#.startswith('crypto'):
                for y,i in enumerate(vka(mp3,5),1):
                    single_msg = types.InlineQueryResultArticle(
                        id=str(y),
                        title=i[1],
                        description=i[0],
                        input_message_content=types.InputTextMessageContent(message_text=str(i[0]) + ' - ' + str(i[1]) + '|' + str(cr(i[2]))),
                        reply_markup=spo)
                    results.append(single_msg)
                bot1.answer_inline_query(q.id, results, cache_time=1)
            else:#.startswith('crypto'):
                SHAZAM=open('music.txt', 'r').read()
                rr=re.findall('[|][\w\d-]+',SHAZAM)
                #rr=random.choice(rr)
                #audio=rr.split('|')[1]
                for i in range(5):
                    single_msg = types.InlineQueryResultCachedAudio(
                        id=str(i),
                        audio_file_id=str(str(random.choice(rr))[1:]),
                        caption='@shazam_downloader',
                        #input_message_content=types.InputTextMessageContent(message_text=str(i[0]) + ' - ' + str(i[1]) + '|' + str(cr(i[2]))),
                        reply_markup=spo)
                    results.append(single_msg)
                bot1.answer_inline_query(q.id, results, cache_time=1)

            '''else:
                y=1
                url = "https://mp3party.net/search?q=" + quote(mp3)
                l2 = dec(str(request.urlopen(url).read()).replace('\\xe2\\x80\\x93','-'))
                tit=re.findall('\/music\/[\d]+">[-\w\d –&#;а-яқғўҳёА-ЯҚҒЎҲЁ]+',str(l2))#
                mp=re.findall('https://dl[\d]+.mp3party.net/online/[\d]+.mp3',str(l2))
                for i in range(len(mp)):
                    t=str(tit[i].split('">')[1]).split(' - ')
                single_msg = types.InlineQueryResultAudio(
                    id=str(y),
                    audio_url='https://z1.fm/download/10981338',
                    title='t',
                    performer='p',
                    caption='@shazam_downloader',#,
                    reply_markup=spo)
                results.append(single_msg)
                bot1.answer_inline_query(q.id, results, cache_time=1)'''

        except Exception as ex:
            bot1.send_message(164135965, str(ex) + '\n\ninline_handler')

    def save(a):
        if not str(a.audio.performer) + ' - ' + str(a.audio.title) in open('music.txt', 'r').read():
            open('music.txt', 'a').write('{} - {}|{}\n'.format(str(a.audio.performer), str(a.audio.title), str(a.audio.file_id)))

    def cr(xx):
      return xx #shifrlash tizimi o'chirib tashlandi

    def rc(xx):
      return xx #shifrlash tizimi o'chirib tashlandi

    def dec(xitoy2):
        cr=['xd0x90', 'xd0xb0', 'xd0x91', 'xd0xb1', 'xd0x92', 'xd0xb2', 'xd0x93', 'xd0xb3', 'xd0x94', 'xd0xb4', 'xd0x95', 'xd0xb5', 'xd0x81', 'xd1x91', 'xd0x96', 'xd0xb6', 'xd0x97', 'xd0xb7', 'xd0x98', 'xd0xb8', 'xd0x99', 'xd0xb9', 'xd0x9a', 'xd0xba', 'xd0x9b', 'xd0xbb', 'xd0x9c', 'xd0xbc', 'xd0x9d', 'xd0xbd', 'xd0x9e', 'xd0xbe', 'xd0x9f', 'xd0xbf', 'xd0xa0', 'xd1x80', 'xd0xa1', 'xd1x81', 'xd0xa2', 'xd1x82', 'xd0xa3', 'xd1x83', 'xd0xa4', 'xd1x84', 'xd0xa5', 'xd1x85', 'xd0xa6', 'xd1x86', 'xd0xa7', 'xd1x87', 'xd0xa8', 'xd1x88', 'xd0xa9', 'xd1x89', 'xd0xaa', 'xd1x8a', 'xd0xab', 'xd1x8b', 'xd0xac', 'xd1x8c', 'xd0xad', 'xd1x8d', 'xd0xae', 'xd1x8e', 'xd0xaf', 'xd1x8f', 'xd2x9a', 'xd2x9b', 'xd2x92', 'xd2x93', 'xd0x8e', 'xd1x9e', 'xd2xb2', 'xd2xb3']
        la=['А', 'а', 'Б', 'б', 'В', 'в', 'Г', 'г', 'Д', 'д', 'Е', 'е', 'Ё', 'ё', 'Ж', 'ж', 'З', 'з', 'И', 'и', 'Й', 'й', 'К', 'к', 'Л', 'л', 'М', 'м', 'Н', 'н', 'О', 'о', 'П', 'п', 'Р', 'р', 'С', 'с', 'Т', 'т', 'У', 'у', 'Ф', 'ф', 'Х', 'х', 'Ц', 'ц', 'Ч', 'ч', 'Ш', 'ш', 'Щ', 'щ', 'Ъ', 'ъ', 'Ы', 'ы', 'Ь', 'ь', 'Э', 'э', 'Ю', 'ю', 'Я', 'я', 'Қ', 'қ', 'Ғ', 'ғ', 'Ў', 'ў', 'Ҳ', 'ҳ']
        xitoy2=xitoy2.replace("\\",'')
        for i in range(74):
          try:
            if cr[i] in xitoy2:
                xitoy2=xitoy2.replace(cr[i],la[i])
          except:
            pass
        return xitoy2

    @bot1.message_handler(func=lambda message: True, content_types=['text', 'photo','sticker','document','video','audio','voice'])
    def main(message):
        fin =1
        chat_id = message.chat.id
        li=['uzhits_net','xitoy2','MP3MEDIANET','reklama_ingliztiliuzz','DOVRONXON','YULDUZ_MUSIC','yoshlar_com','alimiy_677','GrouP_AC','dradiolog','TURKBRENDUZ','Ziyoshkauz','Anhorbek0922','abduganievoff','Velikodushniy','AZARTNIK','Jalol_9933','XaYoT_Officall','ArxivReklama','Inshaalloh_Ubaydullaxoja','Javlon_Akbarov','Price_BassMusic','muztvnet','JAVOKHIROFF_9666','DodasiPRO','Sherzod_Admin','Universalniy_studio','topmuzon_net','Zavqlan_Admin','april20_04uzb','Sardor_Mamadaliyev020AA','yeah1774','Perijo','PARIJDAMAN','Faryod_Com','vodiyuz','EsanoFF','NaturiyJinni','MaxVire','leo_messi_001','ULTRADNIWE','artemnastoyashiy','Jamshid_Admin','skywind','Flyuk','UzLexus','VOYDODA_DESIGN','hamzeh13766','djquvonch','b_nutss','kino_svalka','Behruz_7777','mostmusicPRO','Ilyos_official','Elyorbek96','jerseyzxc','doston4949','Davlat_082','DED_777','Aslanchik0805','azik_singer','Sattorov_Sh','KamranArsenal','Fudbol_Batlle','nTammany','aliuzprod','mybookfun','noviym3','dnechepa','Million_Jam','Bepulrekuz','Musiqa_ru','amsterdamuz','Mashhur_uz','NesoDJ','Sadeecow','Rezcaze','dj_j_shax','BaHoRiM_Tv','milemium6','UlugMedia','Snappy_beatbox','noumo_xb','denisko_0','don_marat','Uzbmp3lar','A_good_person','Davlat_082','senyor07','DeeJay_PM','MUXABATIM','Navoiy_Rap_Mafia','Obmennek','Umidxan_Production','HackerTv','derocker','Uzbmp3lar','NavoUZ','Sultanov77','Musiqa_Tv','Videogramma','AziProduction','yuragimdasan_17','kh_0808','timpure','UZPROBOYS','Videogramma','FAQATKULGU','Shuhratov_javohir_jamshidvich','Uzbegim_Taronasi','Uzbmp3lar','DED_777','notyourdope','shaxrickpro','A_mavlan','Kulinariya','zveruzadmin','Xotin_kere','Bobur_Studio','yozvor','tMyMusic','Rasul_offical','Menedjer_700','photo_design','Meakssks','UzTelegramFm','alec_official','uzxitmuz','makhmudzadee_mtm','AnvarSanayev','ZiyoFerCity','XITBASS','Shaxzodbek777','Dostonnursol','abidov_bahodir','xarxilmavzu','Evro_music1','Guruppalar_No1','MaShXuRsinGeR','TARONAMTV','Qalpoq2000','Show_shu']
        try:
            username = str(message.from_user.username)
        except:
            username = "None"
        if str(message.text) == '/ww':
            SHAZAM=open('music.txt', 'r').read()
            rr=re.findall('[|][\w\d-]+',SHAZAM)
            for i in range(20):
                bot1.send_message(164135965, str(random.choice(rr))[1:])
            #from selenium import webdriver
            #browser = webdriver.Firefox()
            #browser.get('http://seleniumhq.org/')
            #source = requests.get(webLink).text
            #bot1.send_message(chat_id, str(source))
            #i = requests.get("https://mp3party.net/search?q=alisher").text

        if 't.me' in str(message.text) or 'telegram.me' in str(message.text) or '@' in str(message.text):
            bot1.delete_message(chat_id=chat_id, message_id=message.message_id)
        if str(message.text) == '/start':
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            keyboard.add(types.KeyboardButton(text="🔎 Qo'shiq izlash"))
            bot1.send_video(chat_id, 'BAADAgADZQUAAlU4wUjnmjAZJ1B02hYE', caption="Shazam dasturida qidirilgan musiqani yuklash uchun musiqa linkini @shazam_downloader guruhiga ulashing.Tushunmagan bo'lsangiz yuqoridagi videoni tomosha qiling.",reply_markup=keyboard)
        if str(message.text) == "🔎 Qo'shiq izlash":
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="🔎 Qo'shiq izlash", switch_inline_query_current_chat=""))
            bot1.send_message(chat_id, "🔎 Qo'shiq izlash tugmasini bosing va ijrochi yoki qo'shiq nomini yozib 5 sekund kuting",reply_markup=keyboard)
            bot1.delete_message(chat_id=chat_id, message_id=message.message_id)
        if chat_id<0 and bot1.get_chat_members_count(chat_id) > 100 or chat_id == -1001262954594 or username in li:
            if 'Shazam' in str(message.text) and  '. https' in str(message.text) or len(str(message.text))>110:
                name = str(message.text.split('. https')[0])
                try:
                    bot1.send_chat_action(message.chat.id, 'upload_audio')
                    if 'Мое открытие на Shazam' in name:
                        name=str(name[24:])
                        per=name.split(' - ')[0]
                        tit=str(str(name.split(' - ')[1]).split(' ')[0:2]).replace("', '",' ').replace("\", '",' ')[2:-2]
                    if 'I used Shazam to discover ' in name:
                        name=str(name[26:])
                        per=name.split(' by ')[1]
                        tit=str(str(name.split(' by ')[0]).split(' ')[0:2]).replace("', '",' ').replace("\", '",' ')[2:-2]
                    if '-' in str(message.text) and '|' in str(message.text) and len(str(message.text))>110:
                        name=str(message.text).split('|')[0]
                        per = name.split(' - ')[0]
                        tit = name.split(' - ')[1]
                        audi = requests.get(str(rc(str(message.text).split('|')[1]))).content
                        fin=0
                    if name in open('music.txt', 'r').read():
                        SHAZAM=open('music.txt', 'r').read()
                        rr=str(re.findall(name+'[|][\w]+',SHAZAM))[2:-2]
                        audio=rr.split('|')[1]
                        if fin == 0:
                            bot1.send_audio(chat_id, audio=audi, title=tit, performer=per, caption='@shazam_downloader')
                        if ' - ' in rr and not len(str(message.text))>110:
                            per=name.split(' - ')[0]
                            tit=name.split(' - ')[1]#str(rr.split(' - ')[1]).split('|')[0]
                            bot1.send_audio(chat_id,audio=audio,title=tit, performer=per,caption='@shazam_downloader')
                        if ' by ' in rr:
                            per=name.split(' by ')[1]
                            tit=name.split(' by ')[0]#str(rr.split(' - ')[1]).split('|')[0]
                            bot1.send_audio(chat_id,audio=audio,title=tit, performer=per,caption='@shazam_downloader')
                    else:
                        if fin == 0:
                            a=bot1.send_audio(chat_id, audio=audi, title=tit, performer=per,caption='@shazam_downloader')
                            save(a)
                        else:
                            vv=vka(name, 1)
                            if str(vv) == "None" or str(vv) == '[]':# or name.count(' ') > 3:
                                if len(tit) > 40 and len(per) < 30:
                                    tt=str(tit).split(' ')
                                    name=str(per) + ' ' + str(tt[0]) + ' ' + str(tt[1])
                                    vv=vka(name, 1)
                                    audio = requests.get(vv[2]).content
                                    a=bot1.send_audio(chat_id, audio=audio, title=tit, performer=per,caption='@shazam_downloader')
                                    save(a)
                                if len(per) > 40:
                                    tt=str(per).split(' ')
                                    name=str(tt[0]) + ' ' + str(tt[1])
                                    vv=vka(name, 1)
                                    audio = requests.get(vv[2]).content
                                    a=bot1.send_audio(chat_id, audio=audio, title=tit, performer=per,caption='@shazam_downloader')
                                    save(a)
                                else:
                                    bot1.send_message(164135965, 'else' + str(name))
                                    if not name in open('shazam_except.txt', 'r').read():
                                        open('shazam_except.txt', 'a').write(name + '\n')
                                bot1.send_message(164135965, name)
                            else:
                                a=bot1.send_audio(chat_id, audio=requests.get(vv[2]).content, title=tit, performer=per,caption='@shazam_downloader')
                                save(a)
                    bot1.delete_message(chat_id=chat_id, message_id=message.message_id)
                except Exception as ex:
                    bot1.send_message(164135965, str(ex) + '\n\n'+str(message.text))
                    if not name in open('shazam_except.txt', 'r').read():
                        open('shazam_except.txt', 'a').write(name + '\n')
        else:
            bot1.send_message(chat_id, "@shazam_downloader_bot a'zolari 100 dan oshgan guruhlarda ishlaydi")
            #bot1.send_message(chat_id, "Noto'g'ri buyruq berildi")
    bot1.polling()
except:
    bot.send_message(164135965, str(ex))
    bot1.polling()

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
