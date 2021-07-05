import io
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Comic
from .serializers import ComicSerializer
import http.client
from bs4 import BeautifulSoup

@csrf_exempt
def comicApi(request):
    print("hello world!")
    return JsonResponse("cool!", safe=False)

@csrf_exempt
def comicApi(request, name):
    if name == "xkcd":
        perm_link_xkcd, img_url, title, alt, prev_link, next_link = get_page("https://", "xkcd.com", "/")

        # if prev_link exists but prev_id is null create new comic with perm_link only and update prev_id
        # if next_link does not exist in db
        comic_json = populate_comic_json("xkcd", perm_link_xkcd, img_url, title, alt, prev_link, next_link)

        try:
            comic = Comic.objects.get(perm_link=perm_link_xkcd)
            print("Updating comic.")
            comic.next_link = comic_json['next_link']
            comic.save()
            comic_json['id'] = comic.id
            print("Updated comic id: ", comic.id)
        except Comic.DoesNotExist:
            print("Comic did not exist with perm_link: ", perm_link_xkcd)
            comic_serializer = ComicSerializer(data = comic_json)
            if comic_serializer.is_valid():
                comic = comic_serializer.save()
            comic_json['id'] = comic.id
            print("Added comic to database with id:", comic.id)        
        return JsonResponse(comic_json, safe=False)

def get_page(protocol, domain, url):
    conn = http.client.HTTPSConnection(domain)
    conn.request("GET", url)
    response = conn.getresponse()
        
    page_html:str = response.read().decode()
        
    start = page_html.find("Permanent link to this comic:") + 30
    end = page_html.find("<br", start)
    perm_link_xkcd = page_html[start:end]

    start = page_html.find("Image URL (for hotlinking/embedding):") + 38
    end = page_html.find(".png", start)
    img_url = page_html[start:end + 4]

    soup = BeautifulSoup(page_html, features="lxml")
    title = soup.find('div', {"id":"ctitle"}).contents[0]
    alt = soup.find('div', {"id":"comic"}).find('img')['title']
    prev_link = protocol + domain + soup.find('ul', {"class":"comicNav"}).find('a', {"rel":"prev"})['href']

    next = soup.find('ul', {"class":"comicNav"}).find('a', {"rel":"next"})['href']
    if next == "#":
        next_link = ""
    else:
        next_link = protocol + domain + next

    conn.close()
    return perm_link_xkcd,img_url,title,alt,prev_link,next_link

def populate_comic_json(name, perm_link, img_url, title, alt, prev_link, next_link):
    comic_json = {
            'id': '',
            'name': name,
            'title': title,
            'alt': alt,
            'number': 0,
            'date_publish': '1900-01-01',
            'date_crawl': '1900-01-01',
            'img_file': '',
            'perm_link': perm_link,
            'next_link': next_link,
            'prev_link': prev_link,
            'img_url': img_url}
        
    return comic_json
