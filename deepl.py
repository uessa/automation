from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_binary
import pprint
import time

def translate_by_deepl(mytext):
    '''
    DeepLを使った翻訳を行う関数
        入力　翻訳したい英語
        出力　翻訳された日本語
        例外　入力が文字列でない場合
    '''
    if mytext =="":
        return ""
    if type(mytext) is not str:
        raise Exception("文字列ではありません")

    # DeepLのページのURL
    load_url = "https://www.deepl.com/ja/translator"

    # DeepLのページのSelector
    input_selector = ".lmt__textarea.lmt__source_textarea.lmt__textarea_base_style"
    output_selector = ".lmt__textarea.lmt__target_textarea.lmt__textarea_base_style"
    
    '''
    WebDriverの処理がうまくいかなかったら1秒待機して再度WebDriverの処理を行う
    10回Tryしてダメだったらエラーを返して関数処理終
    '''
    err_count=0
    f_succsess=False
    while not f_succsess:
        try: # DeepLにアクセス

            # Chromeのオプションを設定する
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  

            # DockerのSelenium Serverに接続する
            driver = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities=options.to_capabilities(),
                options=options,
            )
            driver.get(load_url)
            f_succsess = True

        except Exception as identifier:
            err_count=err_count+1
            if err_count >=10:
                raise identifier

    #DeepLに英文を送る
    err_count=0
    f_succsess=False
    while not f_succsess:
        try: #DeepLに英文を送る
            en_text_area = driver.find_element(By.CSS_SELECTOR, input_selector) # 英語のテキストエリア
            # en_text_area.clear() # テキストエリアをクリア
            en_text_area.send_keys(mytext) # 翻訳する文字列
            # print(en_text_area.get_attribute("value")) # テキストエリアの値を確認
            print(mytext)
            f_succsess = True

        except Exception  as identifier:              
            err_count=err_count+1
            if err_count >=10:
                raise identifier
            time.sleep(1)

    #フラグ用
    output_before = ""
    while 1:
        err_count=0
        f_succsess=False
        while not f_succsess:
            try:# DeepLの出力を取得する
                # output = driver.find_element(By.CSS_SELECTOR, output_selector).get_attribute("textContent") # 日本語のテキストエリア
                output = driver.find_element(By.CSS_SELECTOR, output_selector).get_attribute("value") # 日本語のテキストエリア
                
                # print(output) # テキストエリアの値を確認
                f_succsess = True
                
            except Exception as identifier:               
                err_count=err_count+1
                if err_count >=10:
                    raise identifier
                time.sleep(1) 
        '''
        取得したoutputが空文字なら、まだ翻訳が終了してないということで、1秒後に再チェック。
        取得したoutputが空文字でない場合、1つ前のoutputと比べて違う内容になってるなら、
        まだ翻訳が終わり切ってないということで1秒後に再チェック。
        取得したoutputが空文字でない場合、1つ前のoutputと同じ内容なら、翻訳終了ということで出力。
        '''        
        if output != "" : #出力が空文字でないとすれば結果の出力が始まった
            time.sleep(10) # 翻訳がn%完了のダイアログ（DeepL）の待機
            if output_before == output:#出力が1つ前の出力と同じなら、出力が完了したってこと
                break
            output_before = output            
        time.sleep(1)

    # 確認用
    print(output)
    print("DeepL Translated")

    #chromeを閉じる
    driver.close()

    #結果出力
    return output

def divide_readable_text(filepath):
    '''
    ファイル（Readable）を英文と区切り文字のリストに分割
        入力　テキストファイルのパス
        出力　英文のリスト，区切り文字のリスト
        
    '''
    with open(filepath, "r", encoding='utf-8') as f:
        data = f.read().splitlines()
        eng_data = [l for i, l in enumerate(data) if ((i%2) == 0)] # 偶数行（英文）のリスト
        sep_data = [l for i, l in enumerate(data) if ((i%2) != 0)] # 奇数行（区切り文字"-----"）のリスト

    return eng_data, sep_data


# pre_text = ["Open your books to page {}.".format(str(i)) for i in range(5) ]
# post_text = [deepl.translate_by_deepl(pre_text[i]) for i in range(5)]

# pprint.pprint(pre_text)
# pprint.pprint(post_text)

# filepath = "/home/muesaka/projects/automation/readable_1-15.txt"
# pre_text, sep_text = deepl.divide_readable_text(filepath)

# print("[{}]".format(pre_text[3]))
# print("[{}]".format(sep_text[3]))