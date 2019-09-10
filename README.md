# つかいかた



## 基本的な使い方

```
#yuki_kawaiuniv <command> args
```

`#yuki_kawaiuniv` の位置は~~どこでもいいです~~ **最初につけてください**



## option付きでcommandを実行

```
#yuki_kawaiuniv <command> -option args
```

`-option` の位置は `args` の前にしてください



## command1の実行結果をcommand2に渡す

```
#yuki_kawaiuniv <command1> [-option1] args | <command2> [-option2] 
```

`(space)|(space)`で `command` をつなぎます



## command1の実行結果にcommand2の実行結果をつなげる

```
#yuki_kawaiuniv <command1> [-option1] args1 + <command2> [-option2] args2
```

`(space)+(space)` で `command` をつなぎます

`result1result2` のようになります





------



- `textimg` , ` imgedit` 以外の全ての `command` は結果を**文字列で**返します
- 改行を含む文字列を引数に渡すときは、**引用符で囲んだ上、文字列 `\n` ではなく改行を含んだ文字列**を書いてください



------



# コマンドたち

------



## 基本操作

### say : オウム返し

```
say arg
```

主に他の `command` に文字列を渡すときにつかいます(あえてこれを使う必要もないのですが)



### textimg : 画像生成

```
textimg arg
```

文字列から黒バックに白文字のpng画像を生成します

改行を含みたい場合は `\n` を記述してください

~~これは `command` をつなげる場合は最後にしてくださいね~~

`imgedit` につなげることができます



### version : バージョン情報

```version
version
```

引数なし。バージョン情報を返します





------



## 機能

### rand : 要素の中から選ぶ

```
rand [-option] arg1 arg2 [arg3 ...]

		-c 		: choice. argsから1つ選ぶ(デフォルト動作)
		-c[num]	: choices. argsから複数選ぶ(同じ要素が複数出る点に注意)
		-s[num]	: sample. argsから複数選ぶ(同じ要素が重複しない点に注意)
		
```

`num` は1~9までしか対応していないので注意

1つの要素は**途中で改行せずに**書いてください



### imgedit : 画像処理

```
imgedit [-option]
		-n			: noise, 画像にノイズをかける(デフォルト動作)
		-g			: gray, 画像をグレースケール化
		-i			: invert, ネガポジ反転
		-m[level]	: mosaic, モザイクをかける 1<level<10
		-R/-G/-B	: R/G/Bに単色化
```

画像を添付してtootすると、処理して返信します

~~単体での使用になります~~

`imgedit` , `textimg` から画像を`|`で渡すことができます

モザイクの `level` は**1<level<10** での指定になります(level=1で無加工, 9～モザイクらしく, 9.99程度で最大限荒く)

同じ数字でも画像のサイズによってモザイクのかかり具合が変わってくるので職人向けかもしれません

`-mosaic` と `level` の間は開けずに入力してください



### drum : 歩くドラム缶の恐怖

```
drum [arg]
```

歩くドラム缶の恐怖

テキストは好みのものに変えられます





------



