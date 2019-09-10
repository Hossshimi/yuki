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
    os.path.abspath(os.path.dirname(__file__)),"NotoSansCJKjp-Medium.otf"))
#print(FONTPATH)
FONTSIZE = 20
COLOR = (255,255,255)


# commands =============================================================
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
    return 0

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

def imgedit(text,in_data):
    mode = "n"    
    if text != None:
        mode = text[1:]
    if in_data != "internal":
        try:
            with urllib.request.urlopen(in_data) as media:
                data = media.read()
                with open("img.png","wb") as f:
                    f.write(data)
        except:
            return "image downroad error!"
    img = Image.open("img.png").convert("RGB")
    img_array = numpy.array(img)
    if mode == "n":
        img_array = img_array.astype("int16")
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                flag = randint(100)
                if flag > 80:
                    noizdiff = (randn(3)*40).astype("int16")
                    img_array[i][j] += noizdiff
                    """rgb = img_array[i,j].astype("float")
                    if rgb[0]+noizdiff[0] > 255:
                        img_array[i,j,0] = numpy.array([255])
                    elif rgb[0]+noizdiff[0] <0:
                        img_array[i,j,0] = numpy.array([0])
                    else:
                        img_array[i,j,0] += noizdiff[0]
                    if rgb[1]+noizdiff[1] > 255:
                        img_array[i,j,1] = numpy.array([255])
                    elif rgb[1]+noizdiff[1] <0:
                        img_array[i,j,1] = numpy.array([0])
                    else:
                        img_array[i,j,1] += noizdiff[1]
                    if rgb[2]+noizdiff[2] > 255:
                        img_array[i,j,2] = numpy.array([255])
                    elif rgb[2]+noizdiff[2] <0:
                        img_array[i,j,2] = numpy.array([0])
                    else:
                        img_array[i,j,2] += noizdiff[2]"""
        img_array = img_array.clip(0,255).astype("uint8")
        result = Image.fromarray(img_array.astype("uint8"))
        result.save("img.png")
    elif mode == "R":
        img_array[:,:,(1,2)] = 0
        result = Image.fromarray(img_array)
        result.save("img.png")
    elif mode == "G":
        img_array[:,:,(0,2)] = 0
        result = Image.fromarray(img_array)
        result.save("img.png")
    elif mode == "B":
        img_array[:,:,(0,1)] = 0
        result = Image.fromarray(img_array)
        result.save("img.png")
    elif mode == "g":
        grey = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1]\
             + 0.114 * img_array[:, :, 2]
        result = Image.fromarray(numpy.uint8(grey))
        result.save("img.png")
    elif mode == "i":
        result = 255 - img_array
        result = Image.fromarray(result)
        result.save("img.png")
    elif "m" in mode:
        level = float(mode[1:])
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
    
def drum(data,option=None,in_data=None):
    if in_data:
        text = "【" + in_data + "】"
    elif data == []:
        text = "【歩くドラム缶の恐怖】"
    else:
        text = "【" + " ".join(data) + "】"
    return text + "\n\n　　　 　}二二{\n　　　 　}二二{\n　　 　　}二二{\n  　  　　  /   ／⌒)\n　　　　| ／ /　/\n　　　　ヽ_｜ /\n　　　　  / ｜｜\n　　　　/　(＿＼\n　　　／ ／　 ﾋﾉ\n　　  / ／\n　　`( ｜\n　  　L/"


