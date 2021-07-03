from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Comic
from .serializers import ComicSerializer


@csrf_exempt
def comicApi(request, comic_id=0):
    if request.method=='GET':
        if comic_id is 0 or comic_id is None:
            comics = Comic.objects.all()
            comic_serializer = ComicSerializer(comics, many=True)
            return JsonResponse(comic_serializer.data, safe=False)
        else:
            comic = Comic.objects.get(id=comic_id)
            comic_serializer = ComicSerializer(comic, many=False)
            return JsonResponse(comic_serializer.data, safe=False)
    elif request.method=='POST':
        comic_data = JSONParser().parse(request)
        comic_serializer = ComicSerializer(data=comic_data)
        if comic_serializer.is_valid():
            comic_serializer.save()
            return JsonResponse("Added successfully!", safe=False)
        return JsonResponse("Failed to add.", safe=False)

#    latest_comic_list = Comic.objects.order_by('-date_publish')[:5]
#    output = ', '.join([c.title for c in latest_comic_list])
#    return HttpResponse(output)
