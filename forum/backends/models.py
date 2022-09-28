from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False

User._meta.get_field('first_name').blank = False
User._meta.get_field('first_name').null = False


class Thread(models.Model):
    title = models.CharField(max_length=500, verbose_name='Article title')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Asked')
    updated_at = models.DateField(auto_now=True, verbose_name='Modified ')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Thread'
        verbose_name_plural = 'Threads'


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    content = models.CharField(max_length=1000, verbose_name='Content')
    created_at = models.DateField(auto_now_add=True, verbose_name='Asked')
    updated_at = models.DateField(auto_now=True, verbose_name='Modified')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
