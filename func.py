#from mastodon import Mastodon
import random
import re
import os
from PIL import Image, ImageDraw, ImageFont
import urllib.request


FONTPATH = os.path.normpath(os.path.join(\
    os.path.abspath(os.path.dirname(__file__)),"VL-Gothic-Regular.ttf"))
#print(FONTPATH)
FONTSIZE = 20
COLOR = (255,255,255)

def help(text,in_data=None):
    return "https://github.com/Hossshimi/yuki"

def say(text,in_data=None):
    if in_data:
        return in_data
    elif text == None:
        return "内容が・・・無いよう！ｗ"
    else:
        return text

def textimg(text,in_data=None):
    #global FONTPATH,FONTSIZE,COLOR
    if in_data:
        text = in_data
    font = ImageFont.truetype(FONTPATH,FONTSIZE)
    width, height = font.getsize_multiline(text)
    bg_ = Image.new("RGB", (width+20,height+20), (0,0,0))
    bg = ImageDraw.Draw(bg_)
    bg.multiline_text((5,5), text, fill=COLOR, font=font)
    bg_.save("img.png")

def rand(text,in_data=None):
    mode = "c"
    if in_data:
        raw = in_data
    else:
        raw = text
    if in_data and re.findall(r"-..?",text):
        raw = text + " " + raw
    if "-c" in raw:
        tmp = re.search(r"(-c\d+)",raw)
        if tmp:
            re.sub(r"\s-c\d+","",raw)
            mode = f"c{raw[2:3]}"
        else:
            raw.replace(" -c","")
    elif "-s" in raw:
        tmp = re.search(r"(-s\d+)",raw)
        if tmp:
            re.sub(r"\s-s\d+","",raw)
            mode = f"s{raw[2:3]}"
        else:
            raw.replace(" -s","")
            mode = "s"

    ulist = raw.split()
    ulist = ulist[1:]

    if "c" in mode:
        if ulist==None: pass
        elif len(mode) > 1:
            modeopt = mode[1] 
            result = random.choices(ulist,k=int(modeopt))
            result = " ".join(result)# + " がいいと思います！"
        else:
            result = random.choice(ulist)# + " がいいと思います！"
    
    elif "s" in mode:
        if ulist==None: pass
        elif len(mode) > 1:
            modeopt = mode[1]
        else: modeopt = 1
        if len(ulist) < modeopt:
            result = "err:rand:選択数が多すぎます"
        else:
            result = random.sample(ulist,int(modeopt))
            result = " ".join(result)# + " がいいと思います！"

    else: result = "err:rand;無効なmodeです"
    
    if ulist==None:
        result = "err:rand:選択肢の指定がありません"
    
    return result

"""def mediaedit(text,url):
    try:
        with urllib.request.urlopen(url) as media:
            data = media.read()
            with open("img.png")"""
