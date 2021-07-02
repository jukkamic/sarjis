from rest_framework import serializers
from sarjis.models import Comic

class ComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = ('id', 'name', 'date_crawl', 'date_publish', 'number', 'title', 'alt', 'img_url')
