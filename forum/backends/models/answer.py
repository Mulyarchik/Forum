from django.conf import settings
from django.db import models

from .question import Question
from .user_voting import Voting


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, verbose_name='question')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    content = models.CharField(max_length=1000, verbose_name='Comment')
    is_useful = models.BooleanField(verbose_name='Is Useful', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Asked')
    voting = models.OneToOneField('Voting', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        ordering = ['is_useful']

    def create(self, question, user, request_post, count_up, count_down):
        if count_up == 0 and count_down == 0:
            new_voting = Voting.objects.create(count_up=count_up, count_down=count_down)

        self.content = request_post['content']
        self.author = user
        self.question = question
        self.voting = new_voting
        super(Answer, self).save(request_post)

    def __str__(self):
        return self.content
