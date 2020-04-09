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

list_ = []
subshflag = False

def transformer(pret):
    global list_
    list_ = []
    #tmp = None

    def depthcount(string):
        fi = re.finditer(r" ",string)
        return str(len(list(fi)))

    def script(index):
        if "chunk" in list_[index]:
            return chunk(index+1)
    
    def chunk(index):
        global result
        if "sentence" in list_[index]:
            return sentence(index+1)
        elif "subshell" in list_[index]:
            return script(index+1)
    
    def sentence(index,pflg=False,res=None):
        global result, subshflag
        
        cmd_ = []
        opt_ = ""
        arg_ = []
        pf = 0
        endflag = False
        count = 0
        lpcnt = 0
        tmp = ""
        while not(endflag):
            opt_ = ""
            arg_ = []
            lpcnt = 0
            for _ in list_[index+count:]:
                if subshflag and (int(depthcount(list_[index+count])) - int(depthcount(list_[index+count+1])) > 3):
                    endflag = True
                    break
                try:
                    if list_[index+count+3]:
                        pass
                except:
                    endflag = True
                    break
                if "command" in list_[index+count]:
                    cmd_.append(list_[index+count+1].split("\t")[1])
                    if cmd_[-1] == "":
                        return None
                    list_[index+count] = ""
                elif "option" in list_[index+count]:
                    opt_ = list_[index+count+1].split("\t")[1]
                    list_[index+count] = ""
                elif ("chars" in list_[index+count]) and ("pipe" in list_[index+count+1]):
                    if pf == 1:
                        pf = 2
                    elif pf == 0:
                        pf = 1
                    count += 1
                    lpcnt += 1
                    break
                elif "arg" in list_[index+count]:
                    try:
                        arg_.append(list_[index+count+1].split("\t")[1])
                        for i_,el in enumerate(list_[index+count+2:]):
                            if ("chars" in el)and(depthcount(list_[index+count+2+i_])==depthcount(list_[index+count+1])):
                                arg_.append(list_[index+count+2+i_].split("\t")[1])
                            elif depthcount(list_[index+count+1]) < depthcount(list_[index+count+2+i_]):
                                pass
                            else: 
                                break
                    except:
                        pass
                    list_[index+count] = ""
                elif "subshell" in list_[index+count]:
                    subshflag = True
                    arg_.append(script(index+count+2))
                    subshflag = False
                elif ("chars" in list_[index+count])and\
                    ("chars" in list_[index+count-1])and\
                    (depthcount(list_[index+count])!=depthcount(list_[index+count-1])):
                    if subshflag:
                        arg_.append(list_[index+count].split("\t")[1])
                        list_[index+count] = ""
                        subshflag = False
                    else:
                        #subshflag = True
                        arg_.append(list_[index+count].split("\t")[1])
                        list_[index+count] = ""
                    count += 1
                    lpcnt += 1
                    break
                count += 1
                lpcnt += 1
            if (pf == 2) and cmd_:
                try:
                    if ("insert" in cmd_[-1]) or ("replace" in cmd_[-1]):
                        tmp = eval(f"func.{cmd_[-1]}(tmp,opt_,arg_)")
                        del cmd_[-1]
                    elif ("imgedit" in cmd_[-1]) and ("u" in opt_):
                        tmp = eval(f"func.imgedit(None,opt_,tootdata[\"media_attachments\"][\"url\"])")
                        del cmd_[-1]
                    elif "imgedit" in cmd_[-1]:
                        tmp = eval(f"func.imgedit(None,opt_)")
                        del cmd_[-1]
                    else:
                        tmp = eval(f"func.{cmd_[-1]}(tmp,opt_)")
                        del cmd_[-1]
                except:
                    tmp = eval(f"func.{cmd_[-1]}(tmp,'None')")
                    del cmd_[-1]
                finally:
                    list_[index+count-lpcnt-1] = ""
            elif cmd_:
                try:
                    if ("insert" in cmd_[-1]):
                        tmp =  eval(f"func.insert(tmp,opt_,' '.join(arg_))")
                    elif ("imgedit" in cmd_[-1]) and ("u" in opt_):
                        tmp = eval(f"func.imgedit(None,opt_,tootdata[\"media_attachments\"][\"url\"])")
                        del cmd_[-1]
                    elif "imgedit" in cmd_[-1]:
                        tmp = eval(f"func.imgedit(None,opt_)")
                        del cmd_[-1]
                    else:
                        tmp = eval(f"func.{cmd_[-1]}(arg_,opt_)")
                        del cmd_[-1]
                except:
                    tmp = eval(f"func.{cmd_[-1]}(arg_,'None')")
                    del cmd_[-1]
                finally:
                    list_[index+count-lpcnt-1] = ""
            if pf == 1:
                pf = 2
        return tmp

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
        if ("yuki_kawaiuniv" in toot["content"]) and not(toot["account"]["acct"]=="yuki"):
            global mastodon, result, tootdata
            tootdata = toot

            shaped = shaper(rawtext=toot["content"], type_="tag")
            # toot内容を整形関数に渡す

            try: 
                tree = LP.parse(shaped)
                pret = tree.pretty(indent_str=" ")
                #print(pret)
                result = transformer(pret)
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