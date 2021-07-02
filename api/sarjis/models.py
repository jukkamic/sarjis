from django.db import models

class Comic(models.Model):
    name = models.CharField(max_length=100)
    date_crawl = models.DateField('date crawled')
    date_publish = models.DateField('date published')
    number = models.IntegerField()
    title = models.CharField(max_length=100)
    alt = models.TextField()
    img_url = models.URLField()

    def __str__(self):
        return (self.name, ": ", self.title, "\n", self.img_url)