import datetime

from django.db import models
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(max_lenght = 100)
    content = models.TextField
    pub_date = models.DateField('data published')

    def __str__(self):
        return self.title
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Category(models.Model):
    title = models.CharField(max_lenght = 100)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_lenght = 20)
    def __str__(self):
        return self.title


class Comment(models.Model):
    pass


class MainMenu(models.Model):
    pass


class Sort(models.Model):
    pass


class Search(models.Model):
    pass