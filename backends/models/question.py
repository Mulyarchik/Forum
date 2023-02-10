from django.db import models, transaction

from .tag import Tag
from .user_voting import User, Voting


class Question(models.Model):
    title = models.CharField(max_length=500, verbose_name='Article title')
    content = models.CharField(max_length=1000, verbose_name='Content')
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Asked')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Modified ')
    tag = models.ManyToManyField(Tag, blank=True)
    voting = models.OneToOneField('Voting', on_delete=models.CASCADE, blank=True, null=True)

    @property
    def total(self):
        return self.voting.count_up + self.voting.count_down

    def get_absolute_url(self):
        return "/questions/%i/" % self.id

    def __str__(self):
        return self.title

    @transaction.atomic
    def create_question(self, user, request_post):
        new_voting = Voting.objects.create(count_up=0, count_down=0)

        self.title = request_post['title']
        self.content = request_post['content']
        self.author = user
        self.voting = new_voting
        super(Question, self).save(request_post)

        for id_tag in request_post.getlist('tags'):
            tag = Tag.objects.get(pk=id_tag)
            self.tag.add(tag)

    @transaction.atomic
    def update(self, user, request_post):
        self.tag.filter(question=self.id).delete()
        self.title = request_post['title']
        self.content = request_post['content']
        self.save(update_fields=['title', 'content'])

        for id_tag in request_post.getlist('tags'):
            tag = Tag.objects.get(pk=id_tag)
            self.tag.add(tag)

    class Meta:
        app_label = 'backends'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
