from django.db import models

from .answer import Answer
from .user_voting import User


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    content = models.CharField(max_length=1000, verbose_name='Comment')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Asked')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def create(self, answer, user, request_post):
        self.content = request_post['content']
        self.author = user
        self.answer = Answer.objects.get(pk=answer)
        super(Comment, self).save(request_post)

    def __str__(self):
        return self.content
