#!/usr/bin/env python 

#
from lxml import html
from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import urlparse
from urllib.parse import urljoin
import re, json, os, shlex, argparse, subprocess


def download_nhk_video(url):

  ua='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

  req = Request(url,data=None,headers={"User-Agent":ua})
  fio = urlopen(req)
  src = fio.read().decode('utf-8')
  tree = html.fromstring(src)


  # iframe へアクセス
  iframe_path = ''
  if tree.xpath('//iframe[@class="video-player"]') :
    ret = tree.xpath('//iframe[@class="video-player"]')
    iframe_path = ret[0].get('src')
  else:
    ret = tree.xpath('//article/script')
    ret = re.search("video:\s*'(.+\.html)'\s*,\s*", ret[0].text)
    iframe_path = "https://www3.nhk.or.jp"+ret[1].replace("\\", "" )

  player_src = urljoin(url, iframe_path)



  req = Request(player_src,data=None,headers={"User-Agent":ua})
  fio = urlopen(req)
  src = fio.read().decode('utf-8')
  tree = html.fromstring(src)
  ## iframe から json URLを取り出し nPlayer になってる
  js = tree.xpath('//script[not(@src) and contains(./text() , "nPlayer")]')[0].text
  json_f_name = re.search("'(\w+\.json)'", js)[1]
  json_url = urljoin(player_src, json_f_name)
  print(json_url)

  # ## 必要なもの取り出し
  req = Request(json_url,data=None,headers={"User-Agent":ua})
  fio = urlopen(req)
  video_json = fio.read().decode('utf-8')
  ret = json.loads(video_json)

  # # m3u8 のURLを取得
  name = os.path.splitext(json_f_name)[0]
  playlist_url = ret["mediaResource"]["url"]
  print(playlist_url)
  title = ret["va"]["adobe"]['vodContentsID']['VInfo1']
  # # ffmpeg でまるっとゲット
  cmd = f"ffmpeg -y -i {playlist_url} -codec copy -f mp4 '{title}-{name}.mp4' "
  print(cmd)
  p1 = subprocess.check_call(shlex.split(cmd))


def main():
  parser = argparse.ArgumentParser(description='NHKニュースの取得')
  parser.add_argument('url', help='ニュースのURL')

  args = parser.parse_args()
  url = vars(args)['url']

  download_nhk_video(url)


#
if __name__ == '__main__':
  main()

