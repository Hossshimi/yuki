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
list_ = []
subshcount = 0
cmd_ = ""
opt_ = {}
arg_ = {}
pflag0 = False
pflag1 = False
subshflag = False

def transformer(pret):
    global result, list_, cmd_, opt_, arg_
    result = ""
    list_ = []
    cmd_ = ""
    opt_ = {}
    arg_ = {}

    def depthcount(string):
        fi = re.finditer(r" ",string)
        return str(len(list(fi)))

    def script(index):
        if "chunk" in list_[index]:
            return chunk(index+1)
    
    def chunk(index):
        global result, pflag0
        if "sentence" in list_[index]:
            #tmp = sentence(index+1)
            #if pflag0:
            #    result = tmp
            return sentence(index+1)
        elif "subshell" in list_[index]:
            return script(index+1)
    
    def sentence(index):
        global cmd_, opt_, arg_, result, subshflag, pflag0, pflag1
        for i,elm in enumerate(list_[index:]):
            try:
                if "pipe" in list_[index+i+1]:
                    pflag0 = True
            except:
                break
            if "command" in elm:
                cmd_ = list_[index+i+1].split("\t")[1]
                #cdelflag = True
            elif "option" in elm:
                if not (depthcount(list_[index+i+1]) in opt_):
                    opt_[depthcount(list_[index+i+1])] = []
                #if "subshell" in l[i+1]:
                #    opt_[depthcount(l[i+1])].append(script(l[i+2:]))
                #else:
                opt_[depthcount(list_[index+i+1])].append(list_[index+i+1].split("\t")[1])
                list_[index+i] = ""
            elif "arg" in elm:
                if not (depthcount(list_[index+i+1]) in arg_):
                    arg_[depthcount(list_[index+i+1])] = []
                #if "subshell" in l[i+1]:
                #    arg_[depthcount(l[i+1])].append(script(l[i+2:]))
                #else:
                try:
                    arg_[depthcount(list_[index+i+1])].append(list_[index+i+1].split("\t")[1])
                except:
                    pass
                list_[index+i] = ""
            elif ("chars" in elm) and ("pipe" in list_[index+i+1]):
                pflag0 = True
                tmp = index+i
                break
            #elif ("chars" in elm) and \
            #    (("subshell" in l[i+1])or("join" in l[i+1])or("pipe" in l[i+1])or("chars" in l[i+1])):
            #    break
            elif "subshell" in elm:
                arg_[depthcount(list_[index+1])].append(script(index+i+2))
            elif ("chars" in list_[index+i]) and ("chars" in list_[index+i-1]):
                if subshflag:
                    arg_[depthcount(list_[index+i])].append(list_[index+i].split("\t")[1])
                    list_[index+i] = ""
                    subshflag = False
                else:
                    subshflag = True
                break
            #elif "sentence" in list_[index+i]
        if pflag0:
            try:
                result = eval(f"func.{cmd_}(arg_[depthcount(list_[index+1])],'{''.join(opt_[depthcount(list_[index+1])])}')",globals(),locals())
            except:
                result = eval(f"func.{cmd_}(arg_[depthcount(list_[index+1])],'None')",globals(),locals())
            finally:
                pflag0 = False
                pflag1 = True
                return sentence(tmp+2)
        elif pflag1:
            pflag1 = False
            try:
                return eval(f"func.{cmd_}(result,'{''.join(opt_[depthcount(list_[index+2])])}')",globals(),locals())
            except:
                return eval(f"func.{cmd_}(result,'None')",globals(),locals())
        else:
            try:
                return eval(f"func.{cmd_}(arg_[depthcount(list_[index+1])],'{''.join(opt_[depthcount(list_[index+1])])}')",globals(),locals())
            except:
                return eval(f"func.{cmd_}(arg_[depthcount(list_[index+1])],'None')",globals(),locals())

    list_ = pret.split("\n")
    return script(1)

"""class T(Transformer):
    def __init__(self):
        global result
        self._command = []
        self._option = []
        self._args = []
        self._sentence_res = None
        self._chunk_res = []
        self.qflag = False

    def sentence(self,tree):
        global result, tootdata, subshcount
        command = self._command.pop()
        try: option = self._option.pop()
        except: option = None
        try:
            if command == None: pass
            elif (command == "imgedit") and ("u" in option): 
                media_url = tootdata["media_attachments"][0]["url"]
                result.append(eval(f"func.imgedit(None,'{option}{media_url}')",globals()))
            elif command == "insert":
                result.append(eval(f"=func.insert('{' '.join(self._args)}','{option}','{result}')",globals(),locals()))
            elif (command == "replace") and (result):
                result.append(eval(f"func.replace(self._args,'{option}',result)",globals(),locals()))
            elif command == "replace":
                result.append(eval(f"func.replace(self._args,'{option}')",globals(),locals()))
            elif result and not(None in result):
                result.append(eval(f"func.{command}(self._args,'{option}')",globals(),locals()))
            else:
                result.append(eval(f"func.{command}(self._args,'{option}')",globals(),locals()))
        except IndexError as e: pass
        except Exception as e:
            result = str(e)
        self._args = []
    
    def allchars(self,tree):
        self.qflag = True

    def command(self,tree):
        try: self._command.append(tree[0].children[0].value)
        except: self._command.append(None)
    
    def option(self,tree):
        if len(self._command) > len(self._option):
            self._option.append(None)
        try: self._option.append(tree[0].children[0].value)
        except: self._option.append(None)
    
    def arg(self,tree):
        global result
        try:
            for v in tree[0].children:
                self._args.append(v.value)
        except: self._args = []
        finally:
            res = result
            if res != None:
                for r in res:
                    if None in self._args:
                        self._args[self._args.index(None)] = r
                        result.remove(r)
    
    def chunk(self,tree):
        global result
        if (type(result) is str):
            self._chunk_res.append(result)
            #if result != 0:
            result.pop()

    def subshell(self,tree):
        global result,subshcount
        try: self._chunk_res.pop()
        except: pass
    
    def script(self,tree):
        global result
        if type(result) is str:
            result.append("".join(self._chunk_res))"""



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
        if ("yuki_kawaiuniv" in toot["content"]) and not(toot["account"]["acct"]=="inori"):
            global mastodon, result, tootdata
            tootdata = toot

            shaped = shaper(rawtext=toot["content"], type_="tag")
            # toot内容を整形関数に渡す

            try: 
                tree = LP.parse(shaped)
                #print(tree.pretty())
                result = []
                T().transform(tree)
            except Exception as e: result = f"Syntax err:※{str(e)}"
            
            try:
                if result != 0: # 出力が文字列の場合
                    if not result:
                        mastodon.status_post(status="何か用？",in_reply_to_id=toot["id"])
                    else:
                        if len(result) < 501:
                            mastodon.status_post(status="".join(result),in_reply_to_id=toot["id"],spoiler_text="result")
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