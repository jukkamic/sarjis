from ..models import Comic
from ..serializers import ComicSerializer
from django.http.response import JsonResponse
from rest_framework import status
from django.conf import settings
import os
import urllib.request
import http.client

class Common():


    @staticmethod    
    def saveImage(img_url:str):
        img_file = img_url.split('/')[-1]
        img_path = settings.IMAGE_ROOT
        img_full_path = os.path.join(img_path, img_file)
        if not os.path.isfile(img_full_path):
            urllib.request.urlretrieve(img_url, img_full_path)   
        return img_file

    @staticmethod    
    def fetchPage(domain:str, path:str):
        conn = http.client.HTTPSConnection(domain)
        conn.request("GET", path)
        response = conn.getresponse()
        page_html:str = response.read().decode()
        conn.close()
        return page_html


