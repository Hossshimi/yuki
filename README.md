<!-- TOC -->

- [つかいかた](#%E3%81%A4%E3%81%8B%E3%81%84%E3%81%8B%E3%81%9F)
    - [基本的な使い方](#%E5%9F%BA%E6%9C%AC%E7%9A%84%E3%81%AA%E4%BD%BF%E3%81%84%E6%96%B9)
    - [オプション付きでコマンドを実行](#%E3%82%AA%E3%83%97%E3%82%B7%E3%83%A7%E3%83%B3%E4%BB%98%E3%81%8D%E3%81%A7%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%82%92%E5%AE%9F%E8%A1%8C)
    - [コマンドの実行結果を別のコマンドに渡す](#%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%81%AE%E5%AE%9F%E8%A1%8C%E7%B5%90%E6%9E%9C%E3%82%92%E5%88%A5%E3%81%AE%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%81%AB%E6%B8%A1%E3%81%99)
    - [~~実行結果をつなげる~~](#%E5%AE%9F%E8%A1%8C%E7%B5%90%E6%9E%9C%E3%82%92%E3%81%A4%E3%81%AA%E3%81%92%E3%82%8B)
    - [引数にスクリプトの結果を埋め込む](#%E5%BC%95%E6%95%B0%E3%81%AB%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%97%E3%83%88%E3%81%AE%E7%B5%90%E6%9E%9C%E3%82%92%E5%9F%8B%E3%82%81%E8%BE%BC%E3%82%80)
    - [Unicodeコードポイントの連続した文字たちを短縮表記](#unicode%E3%82%B3%E3%83%BC%E3%83%89%E3%83%9D%E3%82%A4%E3%83%B3%E3%83%88%E3%81%AE%E9%80%A3%E7%B6%9A%E3%81%97%E3%81%9F%E6%96%87%E5%AD%97%E3%81%9F%E3%81%A1%E3%82%92%E7%9F%AD%E7%B8%AE%E8%A1%A8%E8%A8%98)
- [コマンドたち](#%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%81%9F%E3%81%A1)
    - [基本操作](#%E5%9F%BA%E6%9C%AC%E6%93%8D%E4%BD%9C)
        - [say : オウム返し](#say--%E3%82%AA%E3%82%A6%E3%83%A0%E8%BF%94%E3%81%97)
        - [textimg : 画像生成](#textimg--%E7%94%BB%E5%83%8F%E7%94%9F%E6%88%90)
    - [機能](#%E6%A9%9F%E8%83%BD)
        - [rand : 要素の中から選ぶ](#rand--%E8%A6%81%E7%B4%A0%E3%81%AE%E4%B8%AD%E3%81%8B%E3%82%89%E9%81%B8%E3%81%B6)
        - [imgedit : 画像処理](#imgedit--%E7%94%BB%E5%83%8F%E5%87%A6%E7%90%86)
        - [drum : 歩くドラム缶の恐怖](#drum--%E6%AD%A9%E3%81%8F%E3%83%89%E3%83%A9%E3%83%A0%E7%BC%B6%E3%81%AE%E6%81%90%E6%80%96)
        - [replace : 文字列の置換/削除](#replace--%E6%96%87%E5%AD%97%E5%88%97%E3%81%AE%E7%BD%AE%E6%8F%9B%E5%89%8A%E9%99%A4)
        - [n2c : Unicodeコードポイントで文字指定](#n2c--unicode%E3%82%B3%E3%83%BC%E3%83%89%E3%83%9D%E3%82%A4%E3%83%B3%E3%83%88%E3%81%A7%E6%96%87%E5%AD%97%E6%8C%87%E5%AE%9A)
        - [zwsp : ゼロ幅スペース](#zwsp--%E3%82%BC%E3%83%AD%E5%B9%85%E3%82%B9%E3%83%9A%E3%83%BC%E3%82%B9)
        - [lf : 改行](#lf--%E6%94%B9%E8%A1%8C)
        - [insert : 文字列の指定した位置に文字列挿入](#insert--%E6%96%87%E5%AD%97%E5%88%97%E3%81%AE%E6%8C%87%E5%AE%9A%E3%81%97%E3%81%9F%E4%BD%8D%E7%BD%AE%E3%81%AB%E6%96%87%E5%AD%97%E5%88%97%E6%8C%BF%E5%85%A5)
- [サンプルスクリプト](#%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%97%E3%83%88)
        - [寿司ガチャ](#%E5%AF%BF%E5%8F%B8%E3%82%AC%E3%83%81%E3%83%A3)
        - [ファルコン・ガチャ](#%E3%83%95%E3%82%A1%E3%83%AB%E3%82%B3%E3%83%B3%E3%83%BB%E3%82%AC%E3%83%81%E3%83%A3)
        - [射*カウントダウン](#%E5%B0%84%E3%82%AB%E3%82%A6%E3%83%B3%E3%83%88%E3%83%80%E3%82%A6%E3%83%B3)

<!-- /TOC -->



# つかいかた



## 基本的な使い方

```
#yuki_kawaiuniv <command> <args>
```

`#yuki_kawaiuniv` は**最初につけてください**



## オプション付きでコマンドを実行

```
#yuki_kawaiuniv <command> -<option> <args>
```

`-option` の位置は **`args` の前にしてください**

複数のオプション(たとえば `-a` と `-B`)を同時に指定したい場合は、 `-aB` のように書いてください



## コマンドの実行結果を別のコマンドに渡す

```
#yuki_kawaiuniv <command1> <args> | <command2>
```

`|`で `command` をつなぎます

前後にスペースが無くてもいいです



## ~~実行結果をつなげる~~

~~`+` で `command` をつなぎます~~
~~これも前後のスペースは無くてもいいです~~
~~`result1result2` のようになります~~

-> **!! ver.2では削除されています !!** 

かわりに↓



## 引数にスクリプトの結果を埋め込む

```
command1 arg1_1(command2 arg2)arg1_2
```

`()` でスクリプトを囲んで記述します

**ネスト不可(かっこ内に更にかっこを含めない!)**なのでそこに注意してください





## Unicodeコードポイントの連続した文字たちを短縮表記

```
example1) {A..Z} 
example2) {ぁ..ん}
```

**間に空白が挟まる**ので、不要な場合は後述の`replace`コマンドを使うとよいですよ

example1では`A`から`Z`までの`A B C D ... Z`といったような、
example2では`ぁ`から`ん`までの`ぁ あ ぃ い ... ん`といったような文字列を返します



------



- `textimg` , ` imgedit` 以外の全てのコマンドは結果を**文字列**で返します
- このbotで用いる引用符は**単引用符**ですので、**意図せず二重引用符を用いないように**気を付けてください



------







# コマンドたち

------



## 基本操作

### say : オウム返し

```
say <arg>
```

他の `command` に文字列を渡したりできます(あえてこれを使う必要もないのですが)



### textimg : 画像生成

```
textimg [-option] <arg>
		-b<color>	: 背景色指定, 16進6桁カラーコードで指定('#'不要)
		-t<color>	: 文字色指定, 16進6桁カラーコードで指定('#'不要)
```

文字列から黒バックに白文字(デフォルト色)のpng画像を生成します

`arg` が複数のときは全てを連結させます
スペースを含めたいときは単引用符を使用してください

文字色・背景色を両方指定する場合は**必ず背景色を先に**指定してください

`imgedit` につなげることができます



------



## 機能

### rand : 要素の中から選ぶ

```
rand [-option] <arg1> <arg2> [arg3 ...]

		-C		: Character by character, 引数の文字列を1字ずつに分割して引数とする
		-c 		: choice, argsから1つ選ぶ(デフォルト動作)
		-c<num>	: choices, argsから複数選ぶ(同じ要素が複数出る点に注意)
		-s<num>	: sample, argsから複数選ぶ(同じ要素が重複しない点に注意)
		-i		: int, arg1 <= x <= arg2 を満たす整数を文字列で返す
		-L		: Line feed, 結果を改行で結合(デフォルト動作)
		-S		: Spaced, 結果を空白で結合
		-D		: Delete space, 結果を間隔なしで結合
```

`num` は1~9までしか対応していないので注意

1つの要素は**途中で改行せずに**書いてください



### imgedit : 画像処理

```
imgedit [-option]
		-n			: noise, 画像にノイズをかける
		-g			: gray, 画像をグレースケール化
		-i			: invert, ネガポジ反転
		-m<level>	: mosaic, モザイクをかける 1<level<10
		-R/-G/-B	: R/G/Bに単色化
		-u			: ユーザがアップロードした画像に対して処理を行う
```

**`-u` オプションと共に**画像を添付してtootすると、処理して返信します
(複数添付した場合は1枚目のみ対象となります)

よい例: `imgedit -ui (画像添付)`

**一度に処理できるオプションは`-u`を除き1つ**です
悪い例: `imgedit -uiB`

`imgedit` , `textimg` から画像を`|`で渡すことができます

モザイクの `level` は**1<level<10** での指定になります(level=1で無加工, 9～モザイクらしく, 9.99程度で最大限荒く)
同じ数字でも画像のサイズによってモザイクのかかり具合が変わってくるので職人向けかもしれません
`-m` と `level` の間は開けずに入力してください



### drum : 歩くドラム缶の恐怖

```
drum [arg]
```

歩くドラム缶の恐怖

テキストは好みのものに変えられます



### replace : 文字列の置換/削除

```
replace [-option] <arg> <old> <new> [count]
		-d : delete, 該当文字列を削除(この場合newの指定は不要)
		-r : regular expressions, oldの指定を正規表現で行う
```

`count` で置換回数を指定できます(指定無しの場合全て置換)

他のコマンドから `|` で引数をとった場合、`arg` の位置に挿入されます



### n2c : Unicodeコードポイントで文字指定

```
n2c [-option] <numeral>
	-h : 16進数で指定
	-d : 10進数で指定
```

`option` を指定しない場合は16進数として扱います



### zwsp : ゼロ幅スペース

```
zwsp
```

カスタム絵文字を続けて書くとうまく表示されないことへの対処として実装しました

**コロンとコロンの間に `insert` でこれを挟むことで、隙間を空けずにカスタム絵文字を表示させることができます**



### lf : 改行

```
lf
```

ver.1以降は従来の「単引用符で改行を囲む」という手法が使えなくなったので実装しました



### insert : 文字列の指定した位置に文字列挿入

```
<command> <arg> | insert -<index> <text>
```

**`|` で他のコマンドの結果から文字列を受け取る必要があります**

`index` には整数(負数含む)を指定できます
**文字のカウントは"0文字目"から始まります**
正数 `n` を指定した場合、文字列**始端から** `n-1` 文字目と `n` 文字目の間に挿入されます
負数 `-n` を指定した場合、文字列**終端から** `n-1` 文字目と `n` 文字目の間に挿入されます



------



# サンプルスクリプト

### 寿司ガチャ

```
#yuki_kawaiuniv rand -s4D :sushiset_1: :sushiset_2: :sushiset_3: :sushiset_4: | insert -12 (zwsp) | insert -25 (lf) | insert -38 (zwsp)
```

河井大学(yukiが稼働しているインスタンス)に存在するお寿司4分割絵文字を使用した寿司ガチャができます

うまくお寿司がそろったらたぶんいいことがあります





### ファルコン・ガチャ

```
#yuki_kawaiuniv rand -Cs9D ファルコン・パンチ
```

チ■コ・フルパァンを目指そう！





### 射*カウントダウン

```
#yuki_kawaiuniv say 私が(rand -i 0 9)って言ったら射*していいよ❤じゃあ数えるよ❤(rand -i 0 9)❤(rand -i 0 9)❤(rand -i 0 9)❤(rand -i 0 9)❤(rand -i 0 9)❤(rand -i 0 9)❤(rand -i 0 9)❤(rand -i 0 9)❤(rand -i 0 9)❤(rand -i 0 9)❤❤❤
```

催眠音声の聴きすぎには気を付けよう！