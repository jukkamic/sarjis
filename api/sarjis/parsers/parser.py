from ..serializers import ComicSerializer
from ..models import Comic
from django.http.response import JsonResponse
from rest_framework import status
from .pbf import PbfParser
from .dilbert import DilbertParser
from .smbc import SmbcParser
from .hs import HsParser
from .xkcd import XkcdParser

class Parser():

    @staticmethod
    def parse(name:str, path:str):
        if name=="fingerpori":
            return HsParser.parse(path, "Fingerpori")
        if name=="vw":
            return HsParser.parse(path, "Viivi ja Wagner")
        if name=="velho":
            return HsParser.parse(path, "Velho")
        if name=="fokit":
            return HsParser.parse(path, "Fok_It")
        if name == "xkcd":
            return XkcdParser.parse(path)
        if name=="smbc":
            return SmbcParser.parse(path)
        if name=="dilbert":
            return DilbertParser.parse(path)
        if name=="pbf":
            return PbfParser.parse(path)
        return JsonResponse(data={"content": "No parser found for requested comic: " + name}, 
                            status=status.HTTP_404_NOT_FOUND)

    @staticmethod    
    def updateLinks(name:str, comic:any):
        if not comic.prev_link:
            print("Comic ", comic.name, ",\n", comic.perm_link, ",\nhas no predecessor.")
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
                    print("Invalid serializer for previous comic: ", prev_comic_serializer.errors)
                    return JsonResponse(
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                        data = {"message": "Serializer error handling previous comic",
                            "error": prev_comic_serializer.errors}
                    )
            comic.prev_id = prev_comic.id
            comic.save()
            return JsonResponse(ComicSerializer(comic, many=False).data, safe=False)
