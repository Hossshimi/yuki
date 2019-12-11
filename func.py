#from mastodon import Mastodon
import random as random_
import re
import os
from PIL import Image, ImageDraw, ImageFont
import urllib.request
from io import BytesIO
import numpy
import numpy.random as nprand
import cv2

VERSION = "yuki 1.0.1"

FONTPATH = os.path.normpath(os.path.join(\
    os.path.abspath(os.path.dirname(__file__)),"NotoSansCJKjp-Medium.otf"))
#print(FONTPATH)
FONTSIZE = 20
COLOR = (255,255,255)
var = []


# commands =============================================================
def version(*args):
    return VERSION

def say(arg,option=None):
    #if type(arg) is str:
    #    return arg
    if type(arg) is list:
        return " ".join(arg)
    elif type(arg) is str:
        return arg
    else:
        raise Exception("内容が・・・無いよう！ｗ")

def textimg(arg,option=None):
    global FONTPATH,FONTSIZE,COLOR
    #if type(arg) is str:
    #    text = arg
    if arg:
        text = " ".join(arg)
    else:
        raise Exception("err:textimg:引数の指定なし")
    if "b" in option:
        bgc_h_s = option[option.index("b")+1:option.index("b")+7]
        bgc = (int(bgc_h_s[:2],16),int(bgc_h_s[2:4],16),int(bgc_h_s[4:6],16))
    else: bgc = (0,0,0)
    if "t" in option:
        tc_h_s = option[option.index("t")+1:option.index("t")+7]
        tc = (int(tc_h_s[:2],16),int(tc_h_s[2:4],16),int(tc_h_s[4:6],16))
    else: tc = COLOR
    font = ImageFont.truetype(FONTPATH,FONTSIZE)
    width, height = font.getsize_multiline(text)
    bg_ = Image.new("RGB", (width+20,height+20), bgc)
    bg = ImageDraw.Draw(bg_)
    bg.multiline_text((5,5), text, fill=tc, font=font)
    bg_.save("img.png")
    return 0

def rand(arg,option="None"):
    mode = "c"
    if type(arg) is str:
        ulist = arg.split()
    else:
        ulist = arg
    if option != "None":
        mode = option

    if ("C" in mode): # Cオプションの場合
        ulist =list(" ".join(ulist))

    if "s" in mode:
        if not ulist: pass
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
        elif len(ulist) > 1:
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

def imgedit(arg,option):  
    mode = option
    if "u" in mode:
        try:
            with urllib.request.urlopen(mode[mode.index("h"):]) as media:
                data = media.read()
                with open("img.png","wb") as f:
                    f.write(data)
            mode = mode[:mode.index("h")]
        except:
            raise Exception("err:imgedit:画像取得エラー")
    img = Image.open("img.png").convert("RGB")
    img_array = numpy.array(img)
    if "n" in mode:
        img_array = img_array.astype("int16")
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                flag = nprand.randint(100)
                if flag > 80:
                    noizdiff = (nprand.randn(3)*40).astype("int16")
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
    elif "R" in mode:
        img_array[:,:,(1,2)] = 0
        result = Image.fromarray(img_array)
        result.save("img.png")
    elif "G" in mode:
        img_array[:,:,(0,2)] = 0
        result = Image.fromarray(img_array)
        result.save("img.png")
    elif "B" in mode:
        img_array[:,:,(0,1)] = 0
        result = Image.fromarray(img_array)
        result.save("img.png")
    elif "g" in mode:
        grey = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1]\
             + 0.114 * img_array[:, :, 2]
        result = Image.fromarray(numpy.uint8(grey))
        result.save("img.png")
    elif "i" in mode:
        result = 255 - img_array
        result = Image.fromarray(result)
        result.save("img.png")
    elif "m" in mode:
        level = int(mode[mode.index("m")+1])
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
    
def drum(arg,option="None"):
    if not arg:
        text = "【歩くドラム缶の恐怖】"
    else:
        text = "【" + " ".join(arg) + "】"
    return text + "\n\n　　　 　}二二{\n　　　 　}二二{\n　　 　　}二二{\n  　  　　  /   ／⌒)\n　　　　| ／ /　/\n　　　　ヽ_｜ /\n　　　　  / ｜｜\n　　　　/　(＿＼\n　　　／ ／　 ﾋﾉ\n　　  / ／\n　　`( ｜\n　  　L/"

def replace(arg,option="None",in_data=None):
    count = None
    #if type(arg) is str:
    #    data = arg.split(" ")
    if in_data: arg.insert(0,in_data)
    try:
        if option != "None": opt = option
        else: opt = ""
        text = arg[0]
        old = arg[1]
        if "d" in opt: new = ""
        else: new = arg[2]
        if len(arg) == 4:
            count = int(arg[3])
    except Exception:
        raise Exception("err:replace:引数が足りません")
    if "r" in opt:
        replaced = re.sub(old,new,text)
    else:
        if count:
            replaced = text.replace(old,new,count)
        else:
            replaced = text.replace(old,new)
    return replaced

#def varset(data,option=None,in_data=None):
#    global var
#    if option:
#        option = option[1]
#    if data:
#        if type(data) is list:
#            data = " ".join(data)
#    elif in_data and (in_data != ""):
#        data = in_data
#    if (option) and (int(option) < 10):
#        var[option] = data
#    elif not option:
#        var.append(data)
#    else:
#        raise Exception("err:varset:無効な変数番号")
#    return ""

#def varget(data,option=None,in_data=None):
#    global var
#    if option:
#        option = option[1]
#    if (not option) and len(var) > 0:
#        return var[0]
#    elif (option) and (int(option) < len(var)):
#        return var[int(option)]
#    else:
#        raise Exception("err:varget:無効な変数番号")

def zwsp():
    return chr(8203)

def n2c(data,option="None"):
    if not data:
        raise Exception("err:n2c:コードポイントの指定なし")
    if (type(data) is list) and (len(data)>1):
        raise Exception("err:n2c:無効な数値指定")
    elif type(data) is list: data = data[0]
    if option == "-h": d = int(data,16)
    elif option == "-d": d = int(data)
    elif option: raise Exception("err:n2c:無効なオプション")
    else: d = int(data,16)
    return chr(d)

def insert(data,option=None,in_data=None):
    if (in_data == "None") or (in_data == ""):
        raise Exception("err:insert:対象文字列なし")
    elif (data == "None") or (data == ""):
        raise Exception("err:insert:挿入文字列の指定なし")
    elif (option == "None") or (option == ""):
        raise Exception("err:insert:挿入位置の指定なし")
    if type(data) is list:
        data = " ".join(data)
    if (len(option) > 3) and (option[1] == "-"):
        if option[1:].isnumeric():
            index = int(option[1:])
        else:
            raise Exception("err:insert:無効なインデックス指定")
    elif option.isnumeric():
        index = int(option)
    else:
        raise Exception("err:insert:無効なインデックス指定")
    l = list(in_data)
    l.insert(index,data)
    result = "".join(l)
    return result