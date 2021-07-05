from django.db import models

class Comic(models.Model):
    name = models.CharField(max_length=200)
    date_crawl = models.DateField('date crawled', blank=True, null=True)
    date_publish = models.DateField('date published', blank=True, null=True)
    number = models.IntegerField(null=True)
    title = models.CharField(max_length=200, null=True)
    alt = models.TextField(null=True)
    img_url = models.TextField(null=True)
    prev_link = models.TextField(null=True)
    prev_id = models.IntegerField(null=True)
    next_link = models.TextField(null=True)
    next_id = models.IntegerField(null=True)
    perm_link = models.TextField(unique=True)
    img_file = models.TextField(null=True)