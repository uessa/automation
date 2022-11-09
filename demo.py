from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_binary
import time
import deepl
import pprint

'''
・以下のサイトを参照
    https://qiita.com/Chanmoro/items/9a3c86bb465c1cce738a   # "10分で理解するSelenium"
    https://qiita.com/fujino-fpu/items/e94d4ff9e7a5784b2987 # "PythonとSeleniumでDeepLに英文流して自動翻訳させる"
    https://www.hamlet-engineer.com/posts/DeepL.html        # "Python + Selenium + ChromeでDeepLの翻訳を実行する"

・以下のdockerイメージで動作
    docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:3.141.59-xenon
・コンテナ内で？ブラウザ動作してるからローカルでブラウザ動作の確認ができない
・deepl.py実行時にwarningが出る
    -> demo.pyでdeeplをモジュール読み込みすると出ない？
・while True文 + try exept文でsleep(1)で回してるっぽいので, BOT扱いされちゃうかも？
・text = deepl.TranslationByDeepl(text)でtextが翻訳されて返ってくる

'''

if __name__ == "__main__":

    pre_text = ["Open your books to page {}.".format(str(i)) for i in range(5) ]
    post_text = [deepl.TranslationByDeepL(pre_text[i]) for i in range(5)]

    pprint.pprint(pre_text)
    pprint.pprint(post_text)