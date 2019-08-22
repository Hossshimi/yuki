# つかいかた



## 基本的な使い方

```
#yuki_kawaiuniv <command> args
```

`#yuki_kawaiuniv` の位置はどこでもいいです



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



`textimg` 以外の全ての `command` は結果を**文字列で**返します



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

これは `command` をつなげる場合は最後にしてくださいね



### version : バージョン情報

```version
version
```

引数なし。バージョン情報を返します





------



## 基本機能

### rand : 要素の中から選ぶ

```
rand [-option] arg1 arg2 [arg3 ...]

		-c 		: choice. argsから1つ選ぶ(デフォルト動作)
		-c[num]	: choices. argsから複数選ぶ(同じ要素が複数出る点に注意)
		-s[num]	: sample. argsから複数選ぶ(同じ要素が重複しない点に注意)
		
```

`num` は1~9までしか対応していないので注意



### imgedit : 画像処理

```
imgedit [-option]
			-noise			: 画像にノイズをかける(デフォルト動作)
			-gray			: 画像をグレースケール化
			-inv			: ネガポジ反転
			-mosaic[level]	: モザイクをかける 1<level<10
			-r/-g/-b		: R/G/Bに単色化
```

画像を添付してtootすると、処理して返信します

単体での使用になります

モザイクの `level` は**1<level<10** での指定になります(level=1で無加工, 9~モザイクらしく, 9.99程度で最大限荒く)

`-mosaic` と `level` の間は開けずに入力してください



------



