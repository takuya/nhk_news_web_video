## NHKニュースWEB の動画ニュースを保存してffmpegで遊ぶ

NHK のニュースのTSとm3u8の動画を保存したりしてffmpegで遊ぶ

## install 

```shell
git clone  git@github.com:takuya/nhk_news_web_video.git
cd  nhk_news_web_video
pipenv install 
```
## 使い方 
```
python3  nhk_news_web_video.py https://www3.nhk.or.jp/news/html/20220226/k10013503071000.html
```

## requirements

- python3 lxml
- ffmpeg コマンド

## updates 

- first https://takuya-1st.hatenablog.jp/entry/2018/03/29/234559
- update 2022-02-28 git プロジェクトに

