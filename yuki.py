from mastodon import Mastodon
from mastodon import StreamListener
import os
import re

import func



VERSION = "yuki v0.2.0"



def emptyfunc(*args):
    pass
def version(*args):
    return VERSION

FUNCLIST = {
    "":emptyfunc, #無効なcommandが書かれたときに活躍する
    "help":func.help,
    "version":version,
    "say":func.say,
    "textimg":func.textimg,
    "rand":func.rand,

}

mastodon = None
img_flag = False



def shaper(rawtext,type_): #トゥートを整形する関数
    """if type_ == "conv":
        if rawtext[5] == " ":
            data = rawtext.replace("")
        else:
            data = text[21:]"""
    if type_ == "tag":
        text = rawtext.replace("<p>","")\
                    .replace("</p>","")\
                    .replace("<br />","\n")
        text = re.sub(r'<.+>',"",text)
        if text == "":
            text = "say 内容が・・・無いよう！ｗ"
        if text[0] == " ":
            text = text[1:]
    spltext = text.split(" | ")
    commands = []
    data = []
    for part in spltext:
        commands.append(part.split(" ",maxsplit=1)[0])
        try:
            data.append(part.split(" ",maxsplit=1)[1])
        except:
            data.append(None)
    return commands,data



class MastodonStreamListener(StreamListener):
    def on_update(self,toot): #タグタイムラインが更新されたときの動作
        if "yuki_kawaiuniv" in toot["content"]:
            print(toot["content"])
            global mastodon,img_flag

            shaped = list(shaper(rawtext=toot["content"], type_="tag"))
            #toot内容を整形関数に渡す

            #shaped.append(toot["id"])
            #print(shaped)

            commands_count = len(shaped[0])
            result = None
            for i in range(commands_count): #それぞれのcommandに対して
                if shaped[0][i] in FUNCLIST:
                    if len(shaped[0]) > 1: #commandが複数なら
                        if i == 0: #1つめのcommandの処理なら
                            tmp = FUNCLIST[shaped[0][0]](shaped[1][0])
                        elif i+1 != commands_count: #2回目以降かつ次のcommandがまだ残っているなら
                            if shaped[0][i-1] == "rand":
                                tmp = tmp[:-10]
                            tmp = FUNCLIST[shaped[0][i]](shaped[1][i],in_data=tmp)
                        else: #最後のcommandの処理なら
                            if shaped[0][i-1] == "rand":
                                tmp = tmp[:-10]
                            result = FUNCLIST[shaped[0][i]](shaped[1][i],in_data=tmp)
                            if shaped[0][i] == "textimg":
                                img_flag = True
                    else: #commandが1つなら
                        result = FUNCLIST[shaped[0][0]](shaped[1][0])
                        if shaped[0][i] == "textimg":
                            img_flag = True
                else: #FUNCLISTに指定されたcommandが含まれていないなら
                    result = "err:main:指定されたコマンドは見つかりませんでした..."
            if not img_flag: #出力が文字列の場合
                if result == None:
                    mastodon.status_post(status="何か御用でしょうか？",in_reply_to_id=toot["id"])
                else:
                    mastodon.status_post(status=result,in_reply_to_id=toot["id"])
            else: #出力が画像の場合
                media = mastodon.media_post("img.png",mime_type="image/png")
                mastodon.status_post(status="終わりました！",in_reply_to_id=toot["id"],\
                                        media_ids=media)
                img_flag = False
    #def handle_heartbeat(self): pass



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
    mastodon = login()

    mastodon.status_post(status="@kawai ただいま!",visibility="direct")
    #起動時,開発者にDMを送信

    mastodon.stream_user(MastodonStreamListener(),run_async=False)
    #mastodon.stream_hashtag("yuki_kawaiuniv",MastodonStreamListener(),run_async=False)
    #Streaming APIに接続,タグ"yuki_kawaiuniv"付きのtootを拾う



if __name__ == '__main__':
    main()