import deepl
import glob
import os

'''
・以下のサイトを参照
    https://qiita.com/Chanmoro/items/9a3c86bb465c1cce738a           # "10分で理解するSelenium"
    https://qiita.com/fujino-fpu/items/e94d4ff9e7a5784b2987         # "PythonとSeleniumでDeepLに英文流して自動翻訳させる"
    https://www.hamlet-engineer.com/posts/DeepL.html                # "Python + Selenium + ChromeでDeepLの翻訳を実行する"
    https://yuki.world/python-selenium-chromedriver-auto-update/    # "ChromeDriverを自動更新するPythonライブラリが便利"
・dockerを使う場合は以下で動作
    docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:3.141.59-xenon
・deepl.pyのみを実行時にwarningが出る
    -> demo.pyでdeeplをモジュール読み込みすると出ない

'''

if __name__ == "__main__":

    pre_filepath = glob.glob("*.txt")[0] # 翻訳対象
    post_dir = "./Translated" # 保存先のディレクトリ
    os.makedirs(post_dir, exist_ok=True) # ディレクトリがなければ作る
    post_filepath = "{}/(Translated){}".format(post_dir, pre_filepath) # 保存先のパス

    # 確認
    print("pre_file:   \"{}\"".format(pre_filepath))

    # テキストを分割してリストに
    pre_text, sep_text = deepl.divide_readable_text(pre_filepath) # ファイル（Readable）を英文と区切り文字のリストに分割
    post_text = []

    # deepLでpre_text[]を翻訳しpost_text[]に保存
    for i in range(len(pre_text)):
        # if i == 0:
        #     break
        
        # 翻訳
        post_text.append(deepl.translate_by_deepl(pre_text[i])) # 翻訳した英文を保存
        post_text.append(sep_text[i]) # 区切り文字を保存
        print("{}/{} finished".format(i+1, len(pre_text)))
        print("")
    


    # 翻訳したテキスト（Readable）をファイルに書き込み
    with open(post_filepath, 'w') as f:
        for text in post_text:
            f.write("{}\n".format(text)) # 改行して書き込み

    # 確認
    print("post_file:  \"{}\"".format(post_filepath))

