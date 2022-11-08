from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='tag')
    def __str__(self):
        return '{0} ({1})'.format(self.id, self.name)

class Question(models.Model):
    title = models.CharField(max_length=500, verbose_name='Article title')
    content = models.CharField(max_length=1000, verbose_name='Content')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Asked')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Modified ')
    tag = models.ManyToManyField(Tag, blank=True)
    #question = models.OneToOneField('Voting')

    def get_absolute_url(self):
        return "/questions/%i/" % self.id

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, verbose_name='question')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    content = models.CharField(max_length=1000, verbose_name='Comment')
    is_useful = models.BooleanField(verbose_name='Is Useful', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Asked')
    #answer = models.OneToOneField('Voting')

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        ordering = ['is_useful']

    def __str__(self):
        return self.content


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    content = models.CharField(max_length=1000, verbose_name='Comment')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Asked')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.content


def user_directory_path(instance, filename):
    return 'profile_picture/user_{0}/{1}'.format(instance.id, filename)

class User(AbstractUser):
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    voting = models.ManyToManyField('Vote')

# class Voting(models.Model):
#     result = models.IntegerField

