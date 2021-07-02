from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Comic
from .serializers import ComicSerializer


def index(request):
    latest_comic_list = Comic.objects.order_by('-date_publish')[:5]
    output = ', '.join([c.title for c in latest_comic_list])
    return HttpResponse(output)

@csrf_exempt
def get(request, comic_id):
    comic = Comic.objects.get(id=comic_id)
    comic_serializer = ComicSerializer(comic, many=False)
    return JsonResponse(comic_serializer.data, safe=False)
