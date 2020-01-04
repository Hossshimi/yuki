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



## 実行結果をつなげる

```
#yuki_kawaiuniv <command1> <arg1> + <command2> <arg2>
```

`+` で `command` をつなぎます

これも前後のスペースは無くてもいいです

`result1result2` のようになります



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
- 改行を含む文字列を引数に渡すときは、**引用符で囲んだ上、文字列 `\n` ではなく改行を含んだ文字列**を書いてください



------







# コマンドたち

------



## 基本操作

### say : オウム返し

```
say <arg>
```

他の `command` に文字列を渡したりできます(あえてこれを使う必要もないのですが)



### version : バージョン情報

```version
version
```

引数なし。バージョン情報を返します





------



## 機能

### rand : 要素の中から選ぶ

```
rand [-option] <arg1> <arg2> [arg3 ...]

		-C		: Character by character, 引数の文字列を1字ずつに分割して引数とする
		-c 		: choice, argsから1つ選ぶ(デフォルト動作)
		-c[num]	: choices, argsから複数選ぶ(同じ要素が複数出る点に注意)
		-s[num]	: sample, argsから複数選ぶ(同じ要素が重複しない点に注意)
		-i		: int, arg1 <= x <= arg2 を満たす整数を文字列で返す
		-L		: Line feed, 結果を改行で結合(デフォルト動作)
		-S		: Spaced, 結果を空白で結合
		-D		: Delete space, 結果を間隔なしで結合
		
```

`num` は1~9までしか対応していないので注意

1つの要素は**途中で改行せずに**書いてください



### textimg : 画像生成

```
textimg [-option] <arg>
		-b<color>	: 背景色指定, 16進6桁カラーコードで指定('#'不要)
		-t<color>	: 文字色指定, 16進6桁カラーコードで指定('#'不要)
```

文字列から黒バックに白文字(デフォルト色)のpng画像を生成します

文字色・背景色を両方指定する場合は**必ず背景色を先に**指定してください

`imgedit` につなげることができます



### imgedit : 画像処理

```
imgedit [-option]
		-n			: noise, 画像にノイズをかける(デフォルト動作)
		-g			: gray, 画像をグレースケール化
		-i			: invert, ネガポジ反転
		-m<level>	: mosaic, モザイクをかける 1<level<10
		-R/-G/-B	: R/G/Bに単色化
		-u			: ユーザがアップロードした画像に対して処理を行う
```

**`-u` オプションと共に**画像を添付してtootすると、処理して返信します

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

コロンとコロンの間にこれを挟むことで、隙間を空けずにカスタム絵文字を表示させることができます



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



