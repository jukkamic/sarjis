from rest_framework import serializers
from sarjis.models import Comic

class ComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = ('id', 'name', 'display_name', 'display_source', 'title', 'alt', 'date_publish', 'prev_id', 'next_id', 'prev_link', 'next_link', 'perm_link', 'img_url', 'img_file')
