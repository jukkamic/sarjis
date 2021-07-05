import io
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from rest_framework.fields import empty
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
def getComic(request, name:str, id:int):
    print("getComic() id: ", id)
    comic = Comic.objects.get(id=id)
    print("Loaded comic from db by id: ", comic.id)
    comic_json = populate_comic_json(comic.name, comic.perm_link, comic.img_url, comic.title, comic.alt, comic.prev_link, comic.next_link)
    comic_json['id'] = comic.id
    comic_json['prev_id'] = comic.prev_id
    comic_json['next_id'] = comic.next_id
    return JsonResponse(comic_json, safe=False)

@csrf_exempt
def comicApi(request, name:str):
    perm_link_xkcd, img_url, title, alt, prev_link, next_link = get_page("https://", "xkcd.com", "/")

    # if prev_link exists but prev_id is null create new comic with perm_link only and update prev_id
    # if next_link does not exist in db
    comic_json = populate_comic_json(name, perm_link_xkcd, img_url, title, alt, prev_link, next_link)

    try:
        comic = Comic.objects.get(perm_link=perm_link_xkcd)
        print("Updating comic.")
        comic_json['id'] = comic.id

        prev_id = None

        if prev_link:
            # Provided a previous comic exists fetch it as Comic from db
            try:
                prev_comic = Comic.objects.get(perm_link=prev_link)
                prev_id = prev_comic.id
                if not prev_comic.next_link or not prev_comic.next_id:
                    prev_comic.next_link = perm_link_xkcd
                    prev_comic.next_id = comic.id
                    prev_comic.save()
                    print("Updated previous comic next links")
            except Comic.DoesNotExist:
                # Previous comic not in db. Create it with bare minimum data.
                comic_serializer = ComicSerializer(data = {'next_link': perm_link_xkcd, 
                                                            'next_id': comic.id, 
                                                            'perm_link': prev_link},
                                                            many=False)
                if comic_serializer.is_valid():
                    prev_comic = comic_serializer.save()
                    prev_id = prev_comic.id
                    print("Created previous comic in db with id: ", prev_comic.id)
                else:
                    print("Errors in serializer when creating prev comic: ", comic_serializer.errors)
            comic.prev_id = prev_id
            comic_json['prev_id'] = prev_id
            print("Setting previous comic id to: ", prev_id)
            comic.save()
        print("Updated comic id: ", comic.id)
    except Comic.DoesNotExist:
        print("Comic did not exist with perm_link: ", perm_link_xkcd)
        comic_json['prev_link'] = prev_link
        prev_comic = Comic.objects.get(perm_link=prev_link)
        comic_json['prev_id'] = prev_comic.id
        comic_serializer = ComicSerializer(data = comic_json, many=False)
        if comic_serializer.is_valid():
            comic = comic_serializer.save()
        comic_json['id'] = comic.id
        print("Added comic to database with id:", comic.id)        
#    print("comic_json\n", comic_json)
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
        next_link = None
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
