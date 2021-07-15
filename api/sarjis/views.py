from .parsers.parser import Parser
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework import status
from .models import Comic
from .serializers import ComicSerializer
import json

@csrf_exempt
def getComic(request, name:str, id:int):
    comic = Comic.objects.get(id=id)
    if comic.prev_id is not None:
        return JsonResponse(ComicSerializer(comic, many=False).data, safe=False)
    else:
        return Parser.updateLinks(name, comic)

@csrf_exempt
def getLatest(request, name:str):
    comic_json = Parser.parse(name, "/")
    comic_json['name'] = name
    try:
        comic_from_db = Comic.objects.get(perm_link = comic_json['perm_link'])
        return JsonResponse(ComicSerializer(comic_from_db, many=False).data, safe=False)
    except Comic.DoesNotExist:
        comic_serializer = ComicSerializer(data = comic_json, many=False)
        if comic_serializer.is_valid():
            comic = comic_serializer.save()            
            return Parser.updateLinks(name, comic)
        else:
            print("Invalid serializer for latest comic: ", comic_serializer.errors)
            return JsonResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data = {
                 "message": [{"Invalid serializer for latest comic: ", comic_serializer.errors}]})

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

@csrf_exempt
def getNames(request):
    return JsonResponse(data=Parser.getComicNames(), safe=False)
