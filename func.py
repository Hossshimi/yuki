#from mastodon import Mastodon
import random
import re
import os
from PIL import Image, ImageDraw, ImageFont
import urllib.request
from io import BytesIO
import numpy
import numpy.random as nprand
import cv2

VERSION = "yuki 2.2.4"

FONTPATH = "NotoSansCJKjp-Medium.otf"
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
        return "".join(arg)
    elif type(arg) is str:
        return arg
    else:
        raise Exception("func:say:内容が・・・無いよう！ｗ")

def textimg(arg,option=None):
    global FONTPATH,FONTSIZE,COLOR
    if not option: option = " "
    if type(arg) is list:
        text = "".join(arg)
    elif type(arg) is str:
        text = arg
    else:
        raise Exception("err:textimg:引数の指定なし")
    if "b" in option[0]:
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

def rand(arg,option=None):
    mode = "c"
    if type(arg) is str:
        ulist = arg.split()
    else:
        ulist = arg
    if option != None:
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
            res = random.sample(ulist,int(modev))
            if "L" in mode:
                res = "\n".join(res)
            elif "S" in mode:
                res = " ".join(res)
            elif "D" in mode:
                res = "".join(res)
            else:
                res = "\n".join(res)

    elif "i" in mode:
        if len(ulist) < 2: raise Exception("err:rand:範囲指定が不完全")
        elif len(ulist) > 1:
            res = str(random.randint(int(ulist[0]),int(ulist[1])))

    else:
        if ulist==None: pass
        elif len(mode) > 1:
            modev = mode[mode.index("c")+1] 
            res = random.choices(ulist,k=int(modev))
            if "L" in mode:
                res = "\n".join(res)
            elif "S" in mode:
                res = " ".join(res)
            elif "D" in mode:
                res = "".join(res)
            else:
                res = "\n".join(res)
        else:
            res = random.choice(ulist)
    #else: result = "err:rand:無効なmodeです"
    
    if ulist==None:
        raise Exception("err:rand:選択肢の指定がありません")
    
    return res

def imgedit(arg,option,url=None):  
    mode = option
    if "u" in mode:
        try:
            with urllib.request.urlopen(url) as media:
                data = media.read()
            with open("img.png","wb") as f:
                f.write(data)
            tmp = list(mode)
            tmp.remove("u")
            mode = "".join(tmp)
        except:
            raise Exception("err:imgedit:画像取得エラー")
    img = Image.open("img.png").convert("RGB")
    img_array = numpy.array(img)
    if "n" in mode:
        img_array = img_array.astype("int16")
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                flag = nprand.randint(10)
                if flag > 8:
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

def replace(arg,option=None,in_data=None):
    count = None
    try:
        if option and (option != "None"): opt = option
        else: opt = ""
        if type(arg) is list:
            if in_data: arg.insert(0,in_data)
            text = arg[0]
            old = arg[1]
            new = arg[2]
            try: count = arg[3]
            except: pass
        else:
            text = arg
            old = in_data[0]
            if "d" in opt:
                new = ""
                try: count = in_data[1]
                except: pass
            else:
                new = in_data[1]
                try: count = in_data[2]
                except: pass
    except Exception:
        raise Exception("err:replace:引数エラー")
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

def zwsp(*args):
    return chr(8203)

def lf(*args):
    return "\n"

def n2c(data,option=None):
    if not data:
        raise Exception("err:n2c:コードポイントの指定なし")
    if (type(data) is list) and (len(data)>1):
        raise Exception("err:n2c:無効な数値指定")
    elif type(data) is list: data = data[0]
    if option == "h": d = int(data,16)
    elif option == "d": d = int(data)
    elif option: raise Exception("err:n2c:無効なオプション")
    else: d = int(data,16)
    return chr(d)

def insert(data,option=None,in_data=None):
    if (in_data == None) or (in_data == ""):
        raise Exception("err:insert:対象文字列なし")
    elif (data == None) or (data == ""):
        raise Exception("err:insert:挿入文字列の指定なし")
    elif (option == None) or (option == ""):
        raise Exception("err:insert:挿入位置の指定なし")
    if type(data) is list:
        data = " ".join(data)
    if (len(option) > 1) and (option[1] == "-"):
        if option[1:].isnumeric():
            index = int(option[1:])
        else:
            raise Exception("err:insert:無効なインデックス指定")
    elif option.isnumeric():
        index = int(option)
    else:
        raise Exception("err:insert:無効なインデックス指定")
    l = list(data)
    l.insert(index,in_data)
    result = "".join(l)
    return result

def count(arg,option=None):
    return str(len(arg))

def find(arg,option=None):
    if len(arg) != 2:
        raise Exception("func:find:引数の数が不正")
    if option:
        if not option.isnumeric:
            raise Exception("func:find:不正なoption")
    find_res = list(re.finditer(arg[0],arg[1]))
    num = int(option) if option[0] == "-" else int(option)+1
    if find_res[0] == None:
        res = ""
    elif not option:
        res = str(find_res[0].start())
    else:
        try:
            res = str(find_res[num].start())
        except IndexError:
            raise Exception("func:find:不正なインデックス指定")
    return res