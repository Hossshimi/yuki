#from mastodon import Mastodon
import random as random_
import re
import os
from PIL import Image, ImageDraw, ImageFont
import urllib.request
from io import BytesIO
import numpy
from numpy.random import *
import cv2

FONTPATH = os.path.normpath(os.path.join(\
    os.path.abspath(os.path.dirname(__file__)),"VL-Gothic-Regular.ttf"))
#print(FONTPATH)
FONTSIZE = 20
COLOR = (255,255,255)

def help(*args):
    return "https://github.com/Hossshimi/yuki"

def say(data,option=None,in_data=None):
    if in_data:
        return in_data
    elif data == []:
        return "内容が・・・無いよう！ｗ"
    else:
        return " ".join(data)

def textimg(data,option=None,in_data=None):
    #global FONTPATH,FONTSIZE,COLOR
    if in_data:
        text = in_data
    else:
        text = " ".join(data)
    font = ImageFont.truetype(FONTPATH,FONTSIZE)
    width, height = font.getsize_multiline(text)
    bg_ = Image.new("RGB", (width+20,height+20), (0,0,0))
    bg = ImageDraw.Draw(bg_)
    bg.multiline_text((5,5), text, fill=COLOR, font=font)
    bg_.save("img.png")

def rand_(text,option=None,in_data=None):
    mode = "c"
    if in_data:
        raw = in_data
    else:
        raw = text
    if option:
        mode = option[1:]
    if type(raw) is list:
        ulist = raw
    else:
        ulist = raw.split()
    if "c" in mode:
        if ulist==None: pass
        elif len(mode) > 1:
            modeopt = mode[1] 
            result = random_.choices(ulist,k=int(modeopt))
            result = "\n".join(result)# + " がいいと思います！"
        else:
            result = random_.choice(ulist)# + " がいいと思います！"
    
    elif "s" in mode:
        if ulist==None: pass
        elif len(mode) > 1:
            modeopt = mode[1]
        else: modeopt = 1
        if len(ulist) < int(modeopt):
            result = "err:rand:選択数が多すぎます"
        else:
            result = random_.sample(ulist,int(modeopt))
            result = "\n".join(result)# + " がいいと思います！"

    else: result = "err:rand;無効なmodeです"
    
    if ulist==None:
        result = "err:rand:選択肢の指定がありません"
    
    return result

def imgedit(text,url):
    mode = "noise"    
    if text != None:
        mode = text[1:]
    try:
        with urllib.request.urlopen(url) as media:
            data = media.read()
            with open("img.png","wb") as f:
                f.write(data)
    except:
        return "image downroad error!"
    img = Image.open("img.png").convert("RGB")
    img_array = numpy.array(img)
    #result = Image.fromarray(img_array)
    #result.save("img__.png")
    #numpy.set_printoptions(threshold=4001)
    #print(img_array)
    if mode == "noise":
        #if len(img_array.shape) == 2:
            #grayflag = True
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                flag = randint(100)
                #if flag > 70 and grayflag:
                    #noiz = randint(0,255)
                    #img_array[i,j] = noiz
                if flag > 80:
                    noiz = randint(0,255,3)
                    img_array[i,j] = noiz#[0]
                    #img_array[i,j,1] = noiz[1]
                    #img_array[i,j,2] = noiz[2]
        result = Image.fromarray(img_array)
        result.save("img.png")
    elif mode == "r":
        img_array[:,:,(1,2)] = 0
        result = Image.fromarray(img_array)
        result.save("img.png")
    elif mode == "g":
        img_array[:,:,(0,2)] = 0
        result = Image.fromarray(img_array)
        result.save("img.png")
    elif mode == "b":
        img_array[:,:,(0,1)] = 0
        result = Image.fromarray(img_array)
        result.save("img.png")
    elif mode == "gray":
        grey = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1]\
             + 0.114 * img_array[:, :, 2]
        result = Image.fromarray(numpy.uint8(grey))
        result.save("img.png")
    elif mode == "inv":
        result = 255 - img_array
        result = Image.fromarray(result)
        result.save("img.png")
    elif "mosaic" in mode:
        level = float(mode[6:])
        if level >= 10: return "err:imgedit:無効なlevel"
        ratio = 1 - 0.1*level
        img = cv2.imread("img.png")
        tmp = cv2.resize(img, None, fx=ratio, fy=ratio, \
            interpolation=cv2.INTER_NEAREST)
        result = cv2.resize(tmp, img.shape[:2][::-1], \
            interpolation=cv2.INTER_NEAREST)
        cv2.imwrite("img.png",result)
    else:
        return "err:imgedit:無効なoption"
    return 0
    
