from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from rest_framework.fields import empty
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import status
from .models import Comic
from .serializers import ComicSerializer
import http.client
import urllib.request
import os
from django.conf import settings
from bs4 import BeautifulSoup
import json
from django.core.files.storage import default_storage

@csrf_exempt
def getComic(request, name:str, id:int):
    comic = Comic.objects.get(id=id)
    if comic.prev_id is not None:
        return JsonResponse(ComicSerializer(comic, many=False).data, safe=False)
    else:
        return fetch_prev_and_update_links(name, comic)

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
            return fetch_prev_and_update_links(name, comic)
        else:
            return JsonResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data = {
                 "message": print("Invalid serializer for latest comic: ", comic_serializer.errors)})

@csrf_exempt
def getAllLatest(request):
    fingerpori = getLatest(request, "fingerpori")
    xkcd = getLatest(request, "xkcd")
    smbc = getLatest(request, "smbc")
    vw = getLatest(request, "vw")
    dilbert = getLatest(request, "dilbert")
    velho = getLatest(request, "velho")
    fokit = getLatest(request, "fokit")
    pbf = getLatest(request, "pbf")

    return JsonResponse([
                         json.loads(fingerpori.content),
                         json.loads(vw.content),
                         json.loads(xkcd.content),
                         json.loads(smbc.content),
                         json.loads(dilbert.content),
                         json.loads(velho.content),
                         json.loads(fokit.content),
                         json.loads(pbf.content)
                         ], safe=False)

def fetch_prev_and_update_links(name, comic):
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
#        print("Invalid serializer for previous comic: ", prev_comic_serializer.errors)
        return JsonResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data = {
            "message": print("Invalid serializer for previous comic: ", prev_comic_serializer.errors)})

def parse(name, url):
    if name=="fingerpori":
        return parseHsComic(url, "Fingerpori")
    if name=="vw":
        return parseHsComic(url, "Viivi ja Wagner")
    if name=="velho":
        return parseHsComic(url, "Velho")
    if name=="fokit":
        return parseHsComic(url, "Fok_It")
    if name=="xkcd":
        return parseXkcd(url)
    if name=="smbc":
        return parseSmbc(url)
    if name=="dilbert":
        return parseDilbert(url)
    if name=="pbf":
        return parsePbf(url)

def addComicMeta(name, comic_json):
    comic_json['name'] = name

def parseDilbert(url):
    print("parseDilbert(): ", url)
    conn = http.client.HTTPSConnection("dilbert.com")
    conn.request("GET", url)
    response = conn.getresponse()
    page_html:str = response.read().decode()
    conn.close()

    soup = BeautifulSoup(page_html, features="lxml")

    meta_tag = soup.find("div", attrs={"class": "meta-info-container"})

    if url == "/":
        first_link = meta_tag.find('a', attrs={'class': 'img-comic-link'})
        perm_link = first_link['href']
        return parseDilbert(perm_link)

    perm_link = url
    next_link = None
    prev_link = None

    next_link_tag = soup.find("a", attrs={"class": "js-load-comic-newer"})
    prev_link_tag = soup.find("a", attrs={"class": "js-load-comic-older"})
    if next_link_tag:
        next_link = next_link_tag["href"]
    if prev_link_tag:
        prev_link = prev_link_tag["href"]

    span_tag = meta_tag.find("span", attrs={"class": "comic-rating"})
    date_publish = span_tag.find("div")["data-date"]

    img_url = meta_tag.find("img", attrs={"class": "img-responsive img-comic"})["src"]
    img_file = img_url.split('/')[-1]
    img_path = settings.IMAGE_ROOT
    img_full_path = os.path.join(img_path, img_file)
    if not os.path.isfile(img_full_path):
        urllib.request.urlretrieve(img_url, img_full_path)   

    return {'perm_link': perm_link,
            'img_url': img_url,
            'img_file': img_file,
            'title': "",
            'alt': "",
            'prev_link': prev_link,
            'next_link': next_link,
            'date_publish': date_publish,
            'display_source': 'dilbert.com',
            'display_name': "Dilbert"
            }
    
def parsePbf(url):
    print("parsePbf(): ", url)
    conn = http.client.HTTPSConnection("pbfcomics.com")
    if url != "/":
        url = "/comics/" + url.split("/")[-2] + "/"
    conn.request("GET", url)
    response = conn.getresponse()
    page_html:str = response.read().decode()
    conn.close()

    soup = BeautifulSoup(page_html, features="lxml")

    nav_tag = soup.find("div", attrs={"id": "pbf-bottom-pagination"})

    if url == "/":
        print("get latest comic and parse that")
        perm_link = nav_tag.find("a", attrs={"rel": "latest"})["href"]
        return parsePbf(perm_link)

    title = soup.find("meta", {"property": "og:title"})["content"]

    img_url = soup.find("meta", attrs={"property": "og:image"})["content"]

    perm_link = url
    next_link_tag = nav_tag.find("a", attrs={"rel": "next"})
    prev_link_tag = nav_tag.find("a", attrs={"rel": "prev"})

    next_link = None
    prev_link = None
    if next_link_tag:
        next_link = next_link_tag["href"]
    if prev_link_tag:
        prev_link = prev_link_tag["href"]

    img_file = img_url.split('/')[-1]
    img_path = settings.IMAGE_ROOT
    img_full_path = os.path.join(img_path, img_file)
    if not os.path.isfile(img_full_path):
        urllib.request.urlretrieve(img_url, img_full_path)   

    return {'perm_link': perm_link,
            'img_url': img_url,
            'img_file': img_file,
            'title': title,
            'alt': "",
            'prev_link': prev_link,
            'next_link': next_link,
            'display_source': 'pbfcomics.com',
            'display_name': "The Perry Bible Fellowship"
            }


def parseHsComic(url, comicTitle:str):
    url, page_html = fetchHtmlFromHS(url)

    soup = BeautifulSoup(page_html, features="lxml")

    if url == "/sarjakuvat/":
        perm_link = getPermLinkFromHS(soup, comicTitle)
        return parseHsComic(perm_link, comicTitle)

    perm_link = url

    next_link, prev_link = handleLinksInHS(soup)

    print("handling permalink: ", url)
    print("prev_link", prev_link)
    print("next_link", next_link)

    figure_tag = soup.find("figure", attrs={"class": "cartoon image scroller"})
    if not figure_tag:
        figure_tag = soup.find("figure", attrs={"class": "cartoon image"})        
    img_url= "https:" + figure_tag.find("img")["data-srcset"]
    img_url=img_url.split(" ")[0]
    img_file = img_url.split('/')[-1]
    img_path = settings.IMAGE_ROOT
    img_full_path = os.path.join(img_path, img_file)
    if not os.path.isfile(img_full_path):
        urllib.request.urlretrieve(img_url, img_full_path)   

    date_publish = figure_tag.find("meta", attrs={"itemprop": "datePublished"})["content"]
    print("date_publish: ", date_publish)

    return {'perm_link': perm_link,
            'img_url': img_url,
            'img_file': img_file,
            'title': "",
            'alt': "",
            'prev_link': prev_link,
            'next_link': next_link,
            'date_publish': date_publish,
            'display_source': 'hs.fi',
            'display_name': comicTitle
            }

def handleLinksInHS(soup):
    next_link = soup.find("a", attrs={"class": ["next"]})["href"]
    if next_link == "#":
        next_link = None

    prev_link = soup.find("a", attrs={"class": ["prev"]})["href"]
    if prev_link == "#":
        prev_link = None
    return next_link,prev_link

def getPermLinkFromHS(soup, comicTitle:str):
    cartoons = soup.find("div", attrs={"id": "page-main-content"})
    fp_div = cartoons.find('span', text=comicTitle, attrs = {"class": "title"}).find_parent("div")
    perm_link = fp_div.find(('a'))['href']
    return perm_link

def fetchHtmlFromHS(url):
    if url == "/":
        url = "/sarjakuvat/"
    print("url: ", url)
    conn = http.client.HTTPSConnection("www.hs.fi")
    conn.request("GET", url)
    response = conn.getresponse()
    page_html:str = response.read().decode()
    conn.close()
    return url,page_html

def parseSmbc(url):
    print("parseSmbc(): ", url)
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
    perm_link = "https://" + perm_link.split("//")[-1]
    print("smbc permalink: ", perm_link)
    img_url = soup.find('div', {"id":"cc-comicbody"}).find('img')['src']

    img_path = settings.IMAGE_ROOT
    img_file = img_url.split('/')[-1]
    img_full_path = os.path.join(img_path, img_file)
    if not os.path.isfile(img_full_path):
        urllib.request.urlretrieve(img_url, img_full_path)   

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
    
    print("Smbc")
    print("perm_link: ", perm_link)
    print("prev_link: ", prev_link)
    print("next_link: ", next_link)

    return {'perm_link': perm_link,
            'img_url': img_url,
            'img_file': img_file,
            'title': title,
            'alt': alt,
            'prev_link': prev_link,
            'next_link': next_link,
            'display_name': 'Saturday Morning Breakfast Cereal',
            'display_source': 'smbc-comics.com'}

def parseXkcd(url):
    conn = http.client.HTTPSConnection("xkcd.com")
    conn.request("GET", url)
    response = conn.getresponse()
        
    page_html:str = response.read().decode()
        
    start_perm_link = page_html.find("Permanent link to this comic:") + 30
    end_perm_link = page_html.find("<br", start_perm_link)
    
    start_img = page_html.find("Image URL (for hotlinking/embedding):") + 38
    end_img = page_html.find(".png", start_img)
    soup = BeautifulSoup(page_html, features="lxml")

    perm_link = page_html[start_perm_link:end_perm_link]

    img_path = settings.IMAGE_ROOT
    img_url = page_html[start_img:end_img + 4]
    img_file = img_url.split('/')[-1]
    img_full_path = os.path.join(img_path, img_file)
    if not os.path.isfile(img_full_path):
        urllib.request.urlretrieve(img_url, img_full_path)   

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
            'next_link': next_link,
            'display_name': 'xkcd',
            'display_source': 'xkcd.com'}

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
