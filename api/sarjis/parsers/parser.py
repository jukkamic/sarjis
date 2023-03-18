from .redmeat import RedmeatParser
from .cyanide import CyanideParser
from .luonto import LuontoParser
from .pbf import PbfParser
from .dilbert import DilbertParser
from .smbc import SmbcParser
from .hs import HsParser
from .xkcd import XkcdParser

from ..serializers import ComicSerializer
from ..models import Comic
from django.http.response import JsonResponse
from rest_framework import status
import logging

log = logging.getLogger('sarjis')

class Parser():

    comicSources:any = [
            {
                "name": "fingerpori",
                "title": "Fingerpori",
                "parser": HsParser
            },
            {
                "name": "vw",
                "title": "Viivi ja Wagner",
                "parser": HsParser
            },
            {
                "name": "luonto",
                "title": "Kamala luonto",
                "parser": LuontoParser
            },
            {
                "name": "xkcd",
                "title": "",
                "parser": XkcdParser
            },
            {
                "name": "smbc",
                "title": "",
                "parser": SmbcParser
            },
            # {
            #     "name": "cyanide",
            #     "title": "",
            #     "parser": CyanideParser
            # },
            {
                "name": "fokit",
                "title": "Fok_It",
                "parser": HsParser
            },
            {
                "name": "redmeat",
                "title": "Red Meat",
                "parser": RedmeatParser
            },
            {
                "name": "pbf",
                "title": "",
                "parser": PbfParser
            },
            # {
            #     "name": "velho",
            #     "title": "Velho",
            #     "parser": HsParser
            # }
        ]

    @staticmethod
    def parse(name:str, path:str):
        for source in Parser.comicSources:
            if source['name'] == name:
                try:
                    ret = source['parser'].parse(path, source['title'])            
                except Exception as e:
                    log.exception(e)
                    return JsonResponse(data={"message": str(e)}, status=status.HTTP_204_NO_CONTENT)
                return ret
        return JsonResponse(data={"content": "No parser found for requested comic: " + name}, 
                            status=status.HTTP_404_NOT_FOUND)

    @staticmethod    
    def updateLinks(name:str, comic:any):
        log.debug("update links for " + name)
        if not comic.prev_link:
            log.info("Comic " + comic.name + ",\n" + comic.perm_link + ",\nhas no predecessor.")
            return JsonResponse(ComicSerializer(comic, many=False).data, safe=False)
        else:
            # fetch prev, add current id as next, update prev_id for current
            prev_comic:Comic=None
            try:
                prev_comic = Comic.objects.get(perm_link = comic.prev_link)
                prev_comic.next_id = comic.id
                prev_comic.save()
            except Comic.DoesNotExist:
                prev_comic_json = Parser.parse(name, comic.prev_link)
                prev_comic_json['name'] = name
                prev_comic_json['next_id'] = comic.id

                prev_comic_serializer = ComicSerializer(data = prev_comic_json, many=False)
                if prev_comic_serializer.is_valid():
                    prev_comic = prev_comic_serializer.save()
                else:
                    log.error("Invalid serializer for previous comic: " + prev_comic_serializer.errors)
                    return JsonResponse(
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                        data = {"message": "Serializer error handling previous comic",
                            "error": prev_comic_serializer.errors}
                    )
            comic.prev_id = prev_comic.id
            comic.save()
            return JsonResponse(ComicSerializer(comic, many=False).data, safe=False)

    @staticmethod
    def getComicNames():
        names = []
        for source in Parser.comicSources:
            names.append({'name': source['name']})
        return names