from mastodon import Mastodon
from mastodon import StreamListener
from html.parser import HTMLParser
import os
import re
import shlex
import asyncio
import schedule
import wikipedia
import datetime

import func



VERSION = "yuki v0.4.4"



def emptyfunc(*args):
    pass
def version(*args):
    return VERSION

FUNCLIST = {
    "":emptyfunc, # 無効なcommandが書かれたときに活躍する
    "help":func.help,
    "version":version,
    "say":func.say,
    "textimg":func.textimg,
    "rand":func.rand_,
    "drum":func.drum
}

mastodon = None
img_flag = False



def anniv():
    wikipedia.set_lang("ja")
    t = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    m = t.month
    d = t.day
    raw = wikipedia.page(f"{m}月{d}日").content
    tmp = raw[raw.find("== 記念日")+16:]
    list = tmp[:tmp.find("\n\n\n==")].split("\n")
    text = ""
    for i,part in enumerate(list):
        if i%2 == 0:
            if (len(text)+len(part)) < 501:
                text += ( "<" + part + "> : " )
            else:
                break
        else:
            if (len(text)+len(part)) < 501:
                text += ( part + "\n" )
            else:
                break
    mastodon.status_post(status=text,visibility="unlisted",spoiler_text=f"{m}/{d}になりました！")

def exec(command,data,option,in_data=None): # command実行時の例外をキャッチ
    try:
        #if in_data and (len(command) > 1):
            #for i,c in enumerate(command):
                #FUNCLIST[command[c]](data,in_data) + FUNCLIST[command]
        if in_data:
            return FUNCLIST[command[0]](data,option,in_data)
        else:
            return FUNCLIST[command[0]](data,option)
    except:
        return "err:main:something_went_wrong!"

def shaper(rawtext,type_): # トゥートを整形する関数
    """if type_ == "conv":
        if rawtext[5] == " ":
            data = rawtext.replace("")
        else:
            data = text[21:]"""
    if type_ == "tag":
        parser = Parser()
        parser.feed(rawtext)
        parser.close()
        text = parser.parsed.replace("#yuki_kawaiuniv","",1)
    if text == "":
        text = "say 内容が・・・無いよう！ｗ"
    if text[0] == " ":
        text = text[1:]
    #spltext = text.split(" | ")
    #splspl = []
    #for i,s in spltext:
        #spltext[i] = s.split(" + ")
    spltext = []
    joints = []
    try:
        spl0 = shlex.split(text)
    except:
        spl0 = ["say","err:main:不正な記法です"]
    p_index = 999
    a_index = 999
    for _ in range(spl0.count("|")+spl0.count("+")+1):
        if "|" in spl0:
            p_index = spl0.index("|")
        else:
            p_index = 999
        if "+" in spl0:
            a_index = spl0.index("+")
        else:
            a_index = 999
        if p_index < a_index:
            joints.append("p")
            spltext.append(spl0[:p_index])
            spl0 = spl0[p_index+1:]
        elif p_index > a_index:
            joints.append("a")
            spltext.append(spl0[:a_index])
            spl0 = spl0[a_index+1:]
        elif p_index == a_index:
            spltext.append(spl0)
    if [] in spltext:
        spltext.remove([])
        spltext.append(spl0)
    commands = []
    data = []
    options = []
    o_flag = False
    for part in spltext:
        #sp = part.split(maxsplit=1)
        commands.append(part[0])
        for part_ in part:
            if part_.startswith("-") and len(part_.split()) == 1:
                options.append(part_)
                part.remove(part_)
                o_flag = True
        if not o_flag:
            options.append(None)
        o_flag = False
        try:
            data.append(part[1:])
        except:
            data.append(None)
    return commands,data,joints,options



class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.parsed = ""

    def handle_data(self,data):
        self.parsed += data

    def handle_endtag(self,tag):
        if tag == "p":
            self.parsed += "\n\n"

    def handle_startendtag(self,tag,attrs):
        self.parsed += "\n"



class MastodonStreamListener(StreamListener):
    def on_update(self,toot): # タイムラインが更新されたときの動作
        if ("yuki_kawaiuniv" in toot["content"]) and not(toot["account"]["acct"]=="yuki"):
            #print(toot["content"])
            global mastodon,img_flag

            shaped = shaper(rawtext=toot["content"], type_="tag")
            # toot内容を整形関数に渡す

            commands_count = len(shaped[0])
            result = None
            
            if shaped[0][0] == "imgedit":
                try:
                    url = toot["media_attachments"][0]["url"]
                    res = func.imgedit(shaped[3][0],url)
                    if res != 0:
                        mastodon.status_post(status=res,in_reply_to_id=toot["id"])
                    media = mastodon.media_post("img.png",mime_type="image/png")
                    mastodon.status_post(status="終わりました！",in_reply_to_id=toot["id"],\
                                            media_ids=media,sensitive=True)
                    return 0
                except: 
                    mastodon.status_post(status="画像取得に失敗しました...",in_reply_to_id=toot["id"])
                    return 0
            for i in range(commands_count): # それぞれのcommandに対して
                if shaped[0][i] in FUNCLIST:
                    if len(shaped[0]) > 1: # commandが複数なら
                        if i == 0: # 1つめのcommandの処理なら
                            tmp = exec([shaped[0][0]],shaped[1][0],shaped[3][0])
                        elif i+1 != commands_count: # 2回目以降かつ次のcommandがまだ残っているなら
                            if shaped[2][i-1] == "p": # commandが|で繋がれているなら
                                tmp = exec([shaped[0][i]],shaped[1][i],shaped[3][i],in_data=tmp)
                            elif shaped[2][i-1] == "a" and shaped[1][i]: # +で繋がれ,argがあるなら
                                tmp = tmp + exec([shaped[0][i]],shaped[1][i],shaped[3][i])
                            elif shaped[2][i-1] == "a": # +で繋がれ,argがないなら
                                tmp = tmp + exec([shaped[0][i]],shaped[1][i],shaped[3][i],in_data=tmp)
                        else: # 最後のcommandの処理なら
                            if shaped[2][i-1] == "p": # commandが|で繋がれているなら
                                result = exec([shaped[0][i]],shaped[1][i],shaped[3][i],in_data=tmp)
                            elif shaped[2][i-1] == "a" and shaped[1][i]: # +で繋がれ,argがあるなら
                                result = tmp + exec([shaped[0][i]],shaped[1][i],shaped[3][i])
                            elif shaped[2][i-1]: # +で繋がれ,argがないなら
                                result = tmp + exec([shaped[0][i]],shaped[1][i],shaped[3][i],in_data=tmp)
                            if shaped[0][i] == "textimg":
                                img_flag = True
                    else: # commandが1つなら
                        result = exec([shaped[0][0]],shaped[1][0],shaped[3][0])
                        if shaped[0][i] == "textimg":
                            img_flag = True
                else: # FUNCLISTに指定されたcommandが含まれていないなら
                    result = "err:main:指定されたコマンドは見つかりませんでした..."
            if not img_flag: # 出力が文字列の場合
                if result == None:
                    mastodon.status_post(status="何か御用でしょうか？",in_reply_to_id=toot["id"])
                else:
                    if len(result) < 501:
                        mastodon.status_post(status=result,in_reply_to_id=toot["id"],spoiler_text="result")
                    else:
                        mastodon.status_post(status="結果が500文字を超えています",in_reply_to_id=toot["id"])
            else: # 出力が画像の場合
                media = mastodon.media_post("img.png",mime_type="image/png")
                mastodon.status_post(status="終わりました！",in_reply_to_id=toot["id"],\
                                        media_ids=media,sensitive=True)
                img_flag = False
    def handle_heartbeat(self): # every 15s
        schedule.run_pending()



def login():
    mastodon = Mastodon(
        client_id=os.environ.get("yuki_key"),
        access_token=os.environ.get("yuki_token"),
        client_secret=os.environ.get("yuki_secret"),
        api_base_url = "https://kawaiuniv.work"
    )
    return mastodon



def main():
    global mastodon

    schedule.every().day.at("15:02").do(anniv)

    mastodon = login()
    mastodon.status_post(status="@kawai ただいま！",visibility="direct")
    # 起動時,開発にDMを送信

    mastodon.stream_user(MastodonStreamListener(),run_async=False,reconnect_async=False)
    # Streaming APIに接続,タグ"yuki_kawaiuniv"付きのtootを拾う
    #mastodon.stream_hashtag("yuki_kawaiuniv",MastodonStreamListener(),run_async=False)
    



if __name__ == '__main__':
    main()