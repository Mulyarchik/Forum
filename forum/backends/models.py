from django.conf import settings
from django.db import models
from django.urls import reverse


class Question(models.Model):
    title = models.CharField(max_length=500, verbose_name='Article title')
    content = models.CharField(max_length=1000, verbose_name='Content')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Asked')
    updated_at = models.DateField(auto_now=True, verbose_name='Modified ')

    def get_absolute_url(self):
        #return reverse('post', kwargs={"question_id": self.pk})
        return "/thread/%i/" % self.id

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, verbose_name='question')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    content = models.CharField(max_length=1000, verbose_name='Comment')
    created_at = models.DateField(auto_now_add=True, verbose_name='Asked')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.content
