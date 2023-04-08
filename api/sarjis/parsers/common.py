from django.conf import settings
import os
import urllib.request
import requests
from bs4 import BeautifulSoup
import logging

log = logging.getLogger('sarjis')

class Common():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    @staticmethod    
    def saveImage(img_url:str):
        img_file = img_url.split('/')[-1]
        img_path = settings.MEDIA_ROOT
        if not os.path.exists(img_path):            
            os.mkdir(img_path)
        img_full_path = os.path.join(img_path, img_file)
        if not os.path.isfile(img_full_path):
            try:
                urllib.request.urlretrieve(img_url, img_full_path)
            except Exception as e:
                log.error("Error downloading " + img_url + ": " + img_full_path)
                log.exception(e)
                raise e
        return img_file

    @staticmethod    
    def fetchPage(domain:str, path:str):
        if not domain.startswith("http"):
            domain = "https://" + domain
        if path.startswith("http"):
            domain = ""
        response = requests.get(domain + path, allow_redirects=True)
        page_html:str = response.text
        return page_html

    @staticmethod 
    def getSoup(page_html):
        return BeautifulSoup(page_html, features="html.parser")

