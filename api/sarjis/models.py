from django.db import models

class Comic(models.Model):
    name = models.CharField(max_length=100)
    date_crawl = models.DateField('date crawled', blank=True, null=True)
    date_publish = models.DateField('date published', blank=True, null=True)
    number = models.IntegerField(null=True)
    title = models.CharField(max_length=100, null=True)
    alt = models.TextField(null=True)
    img_url = models.TextField()

    def __str__(self):
        return f'\n{self.name}: {self.title}\n{self.date_crawl}\n{self.img_url}\n'