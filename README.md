notionの各ページに、用語集に書いてある用語にリンクを貼ってくれるツールです。

用語集のリンクはmikan->product->APIの仕様->[用語集](https://www.notion.so/mikantechnology/3e6a181e18a5421fb42d7bf137a6b500?v=29ab01d76c6d4058a1349ee29f8ed90a)

セットアップが少々必要なのでご了承ください。
分からない場合は聞いてください
1. このレポをクローンする
1. PCの環境変数に　名前：NOTION_MIKAN_TOKEN　値：自分のnotionの[アクセストークン](https://docs.google.com/presentation/d/1Tq-C9iTp-ucgSjKgzNVQZipWRN6why6dpBNS21h-AHo/edit#slide=id.g7421994136_0_212)を入れる
1. Python 3をインストールする
1. pipでnotionをインストール (pip install notion)
1. コマンドラインでこのレポのフォルダーに移動 → python main.py --url=Notionのリンク


-------
GAEのCronが動いた時用のメモ

app.yamlはこんな感じ
```
runtime: python37
handlers:
- url: /main
  script: auto
env_variables:
  NOTION_MIKAN_TOKEN: 'V2_TOKEN'
  STORAGE_BUCKET: 'GCPのバケット名'
```