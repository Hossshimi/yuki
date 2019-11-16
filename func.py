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
var = []


# commands =============================================================
def help_(*args):
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
    if ("C" in mode) and (type(raw) is str): # パイプからではなく直接与えられ, Cオプションの場合
        ulist =list(raw)
    elif "C" in mode: # パイプから与えられ, Cオプションの場合
        ulist = list(" ".join(raw))
    elif type(raw) is list: # パイプから与えられ, Cオプションではない場合
        ulist = raw
    else: # パイプからではなく直接与えられ, Cオプションではない場合
        ulist = raw.split()

    if "s" in mode:
        if ulist==None: pass
        elif len(mode) > 1:
            modev = mode[mode.index("s")+1]
        else: modev = 1
        if len(ulist) < int(modev):
            raise Exception("err:rand:選択数が多すぎます")
        else:
            result = random_.sample(ulist,int(modev))
            if "L" in mode:
                result = "\n".join(result)
            elif "S" in mode:
                result = " ".join(result)
            elif "D" in mode:
                result = "".join(result)
            else:
                result = "\n".join(result)

    elif "i" in mode:
        if len(ulist) == 0: pass
        elif len(ulist) >= 2:
            result = str(random_.randint(ulist[0],ulist[1]))

    else:
        if ulist==None: pass
        elif len(mode) > 1:
            modev = mode[mode.index("c")+1] 
            result = random_.choices(ulist,k=int(modev))
            if "L" in mode:
                result = "\n".join(result)
            elif "S" in mode:
                result = " ".join(result)
            elif "D" in mode:
                result = "".join(result)
            else:
                result = "\n".join(result)
        else:
            result = random_.choice(ulist)
    #else: result = "err:rand:無効なmodeです"
    
    if ulist==None:
        raise Exception("err:rand:選択肢の指定がありません")
    
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
        if level >= 10: raise Exception("err:imgedit:無効なlevel")
        ratio = 1 - 0.1*level
        img = cv2.imread("img.png")
        tmp = cv2.resize(img, None, fx=ratio, fy=ratio, \
            interpolation=cv2.INTER_NEAREST)
        result = cv2.resize(tmp, img.shape[:2][::-1], \
            interpolation=cv2.INTER_NEAREST)
        cv2.imwrite("img.png",result)
    else:
        raise Exception("err:imgedit:無効なoption")
    return 0
    
def drum(data,option=None,in_data=None):
    if in_data:
        text = "【" + in_data + "】"
    elif data == []:
        text = "【歩くドラム缶の恐怖】"
    else:
        text = "【" + " ".join(data) + "】"
    return text + "\n\n　　　 　}二二{\n　　　 　}二二{\n　　 　　}二二{\n  　  　　  /   ／⌒)\n　　　　| ／ /　/\n　　　　ヽ_｜ /\n　　　　  / ｜｜\n　　　　/　(＿＼\n　　　／ ／　 ﾋﾉ\n　　  / ／\n　　`( ｜\n　  　L/"

def replace(data,option=None,in_data=None):
    count = None
    if type(data) is str:
        data = data.split(" ")
    try:
        if option:
            opt = option[1:]
        else:
            opt = ""
        if in_data:
            text = in_data
            old = data[0]
            if "d" in opt:
                new = ""
            else:
                new = data[1]
        else:
            text = data[0]
            old = data[1]
            if "d" in opt:
                new = ""
            else:
                new = data[2]
        if (type(data) is list) and (len(data) == 4):
            count = int(data[3])
    except Exception as _:
        raise Exception("err:replace:引数が足りません")
    if "r" in opt:
        replaced = re.sub(old,new,text)
    else:
        if count:
            replaced = text.replace(old,new,count)
        else:
            replaced = text.replace(old,new)
    return replaced

def varset(data,option=None,in_data=None):
    global var
    if option:
        option = option[1]
    if data:
        if type(data) is list:
            data = " ".join(data)
    elif in_data and (in_data != ""):
        data = in_data
    if (option) and (int(option) < 10):
        var[option] = data
    elif not option:
        var.append(data)
    else:
        raise Exception("err:varset:無効な変数番号")
    return ""

def varget(data,option=None,in_data=None):
    global var
    if option:
        option = option[1]
    if (not option) and len(var) > 0:
        return var[0]
    elif (option) and (int(option) < len(var)):
        return var[int(option)]
    else:
        raise Exception("err:varget:無効な変数番号")

def zwsp(**args):
    return chr(8203)

def n2c(data,option=None,in_data=None):
    if data == None:
        raise Exception("err:n2c:コードポイントの指定なし")
    if type(data) is list:
        raise Exception("err:n2c:無効な数値指定")
    if option == "-h":
        d = int(data,16)
    elif option == "-d":
        d = int(data)
    elif option:
        raise Exception("err:n2c:無効なオプション")
    else:
        d = int(data,16)
    return chr(d)