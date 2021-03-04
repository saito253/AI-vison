#!/usr/bin/python3

from urllib import request  # urllib.requestモジュールをインポート
from bs4 import BeautifulSoup  # BeautifulSoupクラスをインポート

url = 'https://packages.debian.org/ja/buster/adduser'
response = request.urlopen(url)
soup = BeautifulSoup(response)
response.close()

print(soup)
