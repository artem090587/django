from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail


class Blog(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='Пользователь')
    subscribers = models.ManyToManyField(User, blank=True, verbose_name='Подписчики', related_name='blogs')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'


class Post(models.Model):
    blog = models.ForeignKey(Blog, verbose_name='Блог')
    title = models.CharField('Заголовок', max_length=255)
    text = models.TextField('Текст')
    created = models.DateTimeField('время создания', auto_now_add=True, db_index=True)
    readers = models.ManyToManyField(User, verbose_name='Кто прочитал', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-created',)


@receiver(post_save, sender=User)
def signal_user(sender, instance, created, **kwargs):
    if created:
        Blog.objects.create(user=instance)


@receiver(post_save, sender=Post)
def signal_post(sender, instance, created, **kwargs):
    if not created:
        return
    emails = instance.blog.subscribers.values_list('email', flat=True)
    username = instance.blog.user.username
    for email in emails:
        if not email:
            continue
        send_mail('Новый пост от {}'.format(username),
                  'Новый пост: {}'.format(instance.title),
                  'noreply@space.com',
                  [email]
                  )


@receiver(m2m_changed, sender=Blog.subscribers.through)
def signal_blog(sender, instance, action, **kwargs):
    if not action == 'post_remove':
        return
    pk_set = kwargs.pop('pk_set')
    Post.readers.through.objects.filter(post__blog_id=instance.user_id, user_id__in=pk_set).delete()


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