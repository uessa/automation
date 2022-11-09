from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_binary
import pprint
import time


'''
DeepLを使った翻訳を行う関数
入力　翻訳したい英語
出力　翻訳された日本語
例外　入力が文字列でない場合
'''

def TranslationByDeepL(mytext):
    if mytext =="":
        return ""
    if type(mytext) is not str:
        raise Exception("文字列ではありません")

    # DeepLのページのURL
    load_url = "https://www.deepl.com/ja/translator"

    # DeepLのページのSelector
    input_selector = ".lmt__textarea.lmt__source_textarea.lmt__textarea_base_style"
    Output_selector = ".lmt__textarea.lmt__target_textarea.lmt__textarea_base_style"
    
    '''
    WebDriverの処理がうまくいかなかったら1秒待機して再度WebDriverの処理を行う
    ただ、10回トライしてダメだったらエラーを返して関数処理終
    以下、WebDriver使うところでは同様の処理
    '''
    errCount=0
    f_succsess=False
    while not f_succsess:
        try: # DeepLにアクセス

            # Chrome のオプションを設定する
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  

            # Selenium Server に接続する
            driver = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities=options.to_capabilities(),
                options=options,
            )
            driver.get(load_url)
            f_succsess = True

        except Exception as identifier:
            errCount=errCount+1
            if errCount >=10:
                raise identifier

    #DeepLに英文を送る
    errCount=0
    f_succsess=False
    while not f_succsess:
        try: #DeepLに英文を送る
            en_text_area = driver.find_element(By.CSS_SELECTOR, input_selector) # 英語のテキストエリア
            en_text_area.clear() # テキストエリアをクリア
            en_text_area.send_keys(mytext) # 翻訳する文字列
            # print(en_text_area.get_attribute("value")) # テキストエリアの値を確認
            f_succsess = True

        except Exception  as identifier:              
            errCount=errCount+1
            if errCount >=10:
                raise identifier
            time.sleep(1)

    #フラグ用
    Output_before = ""
    while 1:
        errCount=0
        f_succsess=False
        while not f_succsess:
            try:# DeepLの出力を取得する
                # Output = driver.find_element(By.CSS_SELECTOR, Output_selector).get_attribute("textContent") # 日本語のテキストエリア
                Output = driver.find_element(By.CSS_SELECTOR, Output_selector).get_attribute("value") # 日本語のテキストエリア
                # print(Output) # テキストエリアの値を確認
                f_succsess = True
                
            except Exception  as identifier:               
                errCount=errCount+1
                if errCount >=10:
                    raise identifier
                time.sleep(1) 
        '''
        取得したoutputが空文字なら、まだ翻訳が終了してないということで、1秒後に再チェック。
        取得したoutputが空文字でない場合、1つ前のoutputと比べて違う内容になってるなら、
        まだ翻訳が終わり切ってないということで1秒後に再チェック。
        取得したoutputが空文字でない場合、1つ前のoutputと同じ内容なら、翻訳終了ということで出力。
        '''        
        if Output != "" : #出力が空文字でないとすれば結果の出力が始まった
            if Output_before == Output:#出力が1つ前の出力と同じなら、出力が完了したってこと
                break
            Output_before = Output            
        time.sleep(1)

    # 確認用
    print("Translation Complite")

    #chromeを閉じる
    driver.close()

    #結果出力
    return Output

if __name__ == "__main__":

    pre_text = ["Open your books to page {}.".format(str(i)) for i in range(5) ]
    post_text = [TranslationByDeepL(pre_text[i]) for i in range(5)]

    pprint.pprint(pre_text)
    pprint.pprint(post_text)