from django.db import models
from django.utils import timezone
from django.shortcuts import reverse


class Blog(models.Model):
    title = models.CharField('Заголовок', max_lenght=100)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'


class Post(models.Model):
    title = models.CharField('Заголовок', max_length=150, db_index=True)
    text = models.TextField('Текст', blank=True, db_index=True)
    slug = models.SlugField(max_length=50, unique=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.title)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse("post_detail_url", kwargs={"slug": self.slug})
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-created',)


class Tag(models.Model):
    title = models.CharField(max_lenght = 20)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return '{}'.format(self.title)


class Comment(models.Model):
    pass


class MainMenu(models.Model):
    pass


class Sort(models.Model):
    pass


class Search(models.Model):
    pass