from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from rest_framework.fields import empty
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Comic
from .serializers import ComicSerializer
import http.client
import urllib.request
import os
from django.conf import settings
from bs4 import BeautifulSoup
import json

@csrf_exempt
def getComic(request, name:str, id:int):
    comic = Comic.objects.get(id=id)
    if comic.prev_id is not None:
        return JsonResponse(ComicSerializer(comic, many=False).data, safe=False)
    else:
        return fetch_prev_update_links(name, comic)

@csrf_exempt
def getLatest(request, name:str):
    comic_json = parse(name, "/")
    addComicMeta(name, comic_json)
    try:
        comic_from_db = Comic.objects.get(perm_link = comic_json['perm_link'])
        return JsonResponse(ComicSerializer(comic_from_db, many=False).data, safe=False)
    except Comic.DoesNotExist:
        comic_serializer = ComicSerializer(data = comic_json, many=False)
        if comic_serializer.is_valid():
            comic = comic_serializer.save()            
            return fetch_prev_update_links(name, comic)
        else:
            print("Invalid serializer for latest comic: ", comic_serializer.errors)

@csrf_exempt
def getAllLatest(request):
    xkcd = getLatest(request, "xkcd")
    smbc = getLatest(request, "smbc")

    return JsonResponse([json.loads(xkcd.content), json.loads(smbc.content)], safe=False)

def fetch_prev_update_links(name, comic):
    # fetch prev, add current id as next, update prev_id for current
    prev_comic_json = parse(name, comic.prev_link)
    addComicMeta(name, prev_comic_json)
    prev_comic_json['next_id'] = comic.id

    prev_comic_serializer = ComicSerializer(data = prev_comic_json, many=False)
    if prev_comic_serializer.is_valid():
        prev_comic = prev_comic_serializer.save()
        comic.prev_id = prev_comic.id
        comic.save()
        return JsonResponse(ComicSerializer(comic, many=False).data, safe=False)
    else:
        print("Invalid serializer for previous comic: ", prev_comic_serializer.errors)

def parse(name, url):
    if name=="xkcd":
        return parseXkcd(url)
    if name=="smbc":
        return parseSmbc(url)

def addComicMeta(name, comic_json):
    comic_json['date_publish'] = '1900-01-01'
    comic_json['date_crawl'] = '1900-01-01'
    comic_json['number'] = 0
    comic_json['name'] = name

def parseSmbc(url):
    if url != "/":
        url = "/comic/" + url.split('/')[-1]
    conn = http.client.HTTPSConnection("www.smbc-comics.com")
    conn.request("GET", url)

    response = conn.getresponse()
    page_html:str = response.read().decode()
    conn.close()

    soup = BeautifulSoup(page_html, features="lxml")

    full_title = soup.find('title').contents[0]
    title = full_title[len("Saturday Morning Breakfast Cereal -"):]

    alt = soup.find('div', {"id":"cc-comicbody"}).find('img')['title']

    perm_link = soup.find('input', {"id":"permalinktext"})['value']
    img_url = soup.find('div', {"id":"cc-comicbody"}).find('img')['src']

    path = os.path.join(settings.BASE_DIR, 'images')
    img_file = img_url.split('/')[-1]
    urllib.request.urlretrieve(img_url, os.path.join(path, img_file))

    prev_element = soup.find('a', {"class":"cc-prev"})
    next_element = soup.find('a', {"class":"cc-next"})

    if prev_element is not None:  
        prev_link = prev_element['href']
    else:
        prev_link = None

    if next_element is not None:  
        next_link = next_element['href']
    else:
        next_link = None
    
    return {'perm_link': perm_link,
            'img_url': img_url,
            'img_file': img_file,
            'title': title,
            'alt': alt,
            'prev_link': prev_link,
            'next_link': next_link}

def parseXkcd(url):
    conn = http.client.HTTPSConnection("xkcd.com")
    conn.request("GET", url)
    response = conn.getresponse()
        
    img_path = os.path.join(settings.BASE_DIR, 'images')

    page_html:str = response.read().decode()
        
    start_perm_link = page_html.find("Permanent link to this comic:") + 30
    end_perm_link = page_html.find("<br", start_perm_link)
    
    start_img = page_html.find("Image URL (for hotlinking/embedding):") + 38
    end_img = page_html.find(".png", start_img)
    soup = BeautifulSoup(page_html, features="lxml")

    perm_link = page_html[start_perm_link:end_perm_link]
    img_url = page_html[start_img:end_img + 4]
    img_file = img_url.split('/')[-1]
    urllib.request.urlretrieve(img_url, os.path.join(img_path, img_file))   
    title = soup.find('div', {"id":"ctitle"}).contents[0]
    alt = soup.find('div', {"id":"comic"}).find('img')['title']
    prev_element = soup.find('ul', {"class":"comicNav"}).find('a', {"rel":"prev"})
    if prev_element is not None:
        prev_link = prev_element['href']
    else:
        prev_link = None

    next = soup.find('ul', {"class":"comicNav"}).find('a', {"rel":"next"})['href']
    if next == "#":
        next_link = None
    else:
        next_link = next

    conn.close()
    return {'perm_link': perm_link,
            'img_url': img_url,
            'img_file': img_file,
            'title': title,
            'alt': alt,
            'prev_link': prev_link,
            'next_link': next_link}

def populate_comic_json(name, perm_link, img_url, img_file, title, alt, prev_link, next_link):
    comic_json = {
            'id': '',
            'name': name,
            'title': title,
            'alt': alt,
            'number': 0,
            'date_publish': '1900-01-01',
            'date_crawl': '1900-01-01',
            'img_file': img_file,
            'perm_link': perm_link,
            'next_link': next_link,
            'prev_link': prev_link,
            'img_url': img_url}
        
    return comic_json
