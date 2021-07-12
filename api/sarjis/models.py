from django.db import models

class Comic(models.Model):
    name = models.CharField(max_length=100)
    display_name =  models.CharField(max_length=100)
    display_source = models.CharField(max_length=100)
    date_publish = models.DateField(blank=True, null=True)
    title = models.TextField(null=True, blank=True)
    alt = models.TextField(null=True, blank=True)
    img_url = models.TextField(null=True)
    prev_link = models.TextField(null=True)
    prev_id = models.IntegerField(null=True)
    next_link = models.TextField(null=True)
    next_id = models.IntegerField(null=True)
    perm_link = models.TextField(unique=True)
    img_file = models.TextField(null=True)
