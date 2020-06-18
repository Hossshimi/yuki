#!/usr/bin/env python3

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

from lark import Lark, Transformer

import func



with open("Grammar.lark",encoding="utf-8") as grammar:
    LP = Lark(grammar.read(),start="script")



result = ""

class T(Transformer):
    def __init__(self):
        self._sentence_res = None
        self._chunk_res = []
        self._tmp_res = []
        self.qflag = False

    def sentence(self,tree):
        global tootdata
        opt = None
        arg = []
        for tr in tree:
            try:
                if tr.value: break
            except: pass
            if tr.data == "command":
                cmd = tr.children[0].children[0].value
            elif tr.data == "option":
                opt = tr.children[0].children[0].value
            elif tr.data == "arg":
                for t in tr.children:
                    if t == None:
                        arg.append(self._tmp_res.pop(0))
                    else:
                        arg.append(t.children[0].value)
        if (not arg) and not(cmd in ["version","lf","zwsp"]): arg.append(self._tmp_res.pop())
        elif not arg: arg = None
        try:
            if cmd == None: pass
            elif (cmd == "imgedit") and ("u" in opt): 
                media_url = tootdata["media_attachments"][0]["url"]
                res = eval(f"func.imgedit(None,opt+media_url)")
            elif cmd == "insert":
                res = eval(f"func.insert(arg,opt,self._tmp_res)")
            elif (cmd == "replace") and (self._tmp_res):
                res = eval(f"func.replace(arg,opt,self._tmp_res)")
            elif cmd == "replace":
                res = eval(f"func.replace(arg,opt)")
            else:
                res = eval(f"func.{cmd}(arg,opt)")
        except Exception as e:
            res = str(e)
        self._tmp_res.append(res)

    def subshell(self,tree):
        pass
    
    def script(self,tree):
        global result
        if type(self._tmp_res[-1]) is int: result = 0
        else: result = "".join(self._tmp_res)



mastodon = None
tootdata = None



def anniv():
    wikipedia.set_lang("ja")
    t = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    m = t.month
    d = t.day
    raw = wikipedia.page(f"{m}月{d}日").content
    tmp = raw[raw.find("== 記念日")+15:]
    list_ = tmp[:tmp.find("\n\n\n==")].split("\n")
    text = ""
    for part in list_:
        if (len(text)+len(part)) < 499:
            text += (part + "\n")
        else:
            break
    mastodon.status_post(status=text,visibility="unlisted",spoiler_text=f"{m}/{d}～")



def shaper(rawtext,type_): # トゥートを整形する関数
    if type_ == "tag":
        parser = Parser()
        parser.feed(rawtext)
        parser.close()
        text = parser.parsed.replace("#yuki_kawaiuniv","",1)
    if text == "":
        text = "say 内容が・・・無いよう！ｗ"
    if text[0] == " ":
        text = text[1:]
    for sh in re.finditer(r"\{.\.\..\}",text):
        frm = ord(sh.group()[1])
        to = ord(sh.group()[4])
        unf_list = list(map(lambda n: chr(n), list(range(frm,to+1))))
        unf = " ".join(unf_list)
        text = text[:sh.span()[0]] + unf + text[sh.span()[1]:]
    return text



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
            global mastodon, result, tootdata
            tootdata = toot

            shaped = shaper(rawtext=toot["content"], type_="tag")
            # toot内容を整形関数に渡す

            try: 
                tree = LP.parse(shaped)
                T().transform(tree)
            except Exception as e:
                result = f"err:※{str(e)}"
            
            try:
                if result != 0: # 出力が文字列の場合
                    if not result:
                        mastodon.status_post(status="何か用？",in_reply_to_id=toot["id"])
                    else:
                        if len(result) < 501:
                            mastodon.status_post(status=result,in_reply_to_id=toot["id"],spoiler_text="result")
                        else:
                            mastodon.status_post(status="結果が500文字を超えてます",in_reply_to_id=toot["id"])
                else: # 出力が画像の場合
                    media = mastodon.media_post("img.png",mime_type="image/png")
                    mastodon.status_post(status="終わり！",in_reply_to_id=toot["id"],\
                                            media_ids=media,sensitive=True)
            except Exception as e:
                mastodon.status_post(status=str(e),in_reply_to_id=toot["id"])
        func.var = []

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