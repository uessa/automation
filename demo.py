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

    filepath = "/home/muesaka/projects/automation/readable_1-15"
    pre_filepath = filepath + ".txt"
    post_filepath = filepath + "_translated.txt"

    pre_text, sep_text = deepl.divide_readable_text(pre_filepath) # ファイル（Readable）を英文と区切り文字のリストに分割
    post_text = []

    # deepLでpre_text[]を翻訳しpost_text[]に保存
    for i in range(len(pre_text)):
        # if i == 5:
        #     break
        
        post_text.append(deepl.translate_by_deepl(pre_text[i])) # 翻訳した英文を保存
        post_text.append(sep_text[i]) # 区切り文字を保存
        print("{}/{} finished".format(i+1, len(pre_text)))
        print("")

    # 翻訳したテキスト（Readable）をファイルに保存
    with open(post_filepath, 'w') as f:
        for text in post_text:
            f.write("{}\n".format(text)) # 改行して保存

