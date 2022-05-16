from django.conf import settings
import os
import urllib.request
import requests

class Common():

    @staticmethod    
    def saveImage(img_url:str):
        img_file = img_url.split('/')[-1]
        img_path = settings.MEDIA_ROOT
        img_full_path = os.path.join(img_path, img_file)
        if not os.path.isfile(img_full_path):
            urllib.request.urlretrieve(img_url, img_full_path)   
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


