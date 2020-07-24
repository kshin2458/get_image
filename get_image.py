import requests
import random
import shutil
import bs4
import ssl
import os
import logging
logging.basicConfig(level=logging.INFO)

ssl._create_default_https_context=ssl._create_unverified_context

class ImageScraping():
    def __init__(self, file_path=None):
        self.file_path=file_path if file_path else "./"
        if not os.path.isdir(self.file_path):
            os.mkdir(self.file_path)
    
    def get_urls(self, keyword):
        Res = requests.get("https://www.google.com/search?hl=jp&q=" + keyword + "&btnG=Google+Search&tbs=0&safe=off&tbm=isch")
        Html = Res.text
        Soup = bs4.BeautifulSoup(Html,'html.parser')
        links = Soup.find_all("img", limit=40)
        urls=[]
        for info in links:
            urls.append(info.get("src"))
        urls=urls[1:]
        return urls

    def download_img(self, keyword=None, file_name="image"):
        if not keyword:
            logging.error("検索ワード(keyword)が指定されていません。")

        urls = self.get_urls(keyword)
        num=0
        file_name=self.file_path+file_name
        while True:
            if os.path.isfile(file_name+str(num)+".jpg"):
                num=num+1
            else:
                break
        
        for url in urls:
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(file_name+str(num)+".jpg", 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                num=num+1
        print("finish!")

if __name__=="__main__":
    keyword = input("検索ワード:")
    file_name = input("ファイル名:")
    imgscr=ImageScraping(file_path="./image/")
    imgscr.download_img(keyword=keyword, file_name=file_name)
