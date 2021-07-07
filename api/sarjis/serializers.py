from rest_framework import serializers
from sarjis.models import Comic

class ComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = ('id', 'name', 'date_crawl', 'date_publish', 'number', 'title', 'alt', 'img_url', 'prev_link', 'next_link', 'next_id', 'prev_id', 'perm_link', 'img_file')
