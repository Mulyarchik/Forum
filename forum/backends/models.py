from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.db.models import F


class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='tag')

    class Meta:
        app_label = 'backends'

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.name)


class Question(models.Model):
    title = models.CharField(max_length=500, verbose_name='Article title')
    content = models.CharField(max_length=1000, verbose_name='Content')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
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
    def create_question(self, user, request_post, count_up, count_down):
        if count_up == 0 and count_down == 0:
            new_voting = Voting.objects.create(count_up=count_up, count_down=count_down)

        self.title = request_post['title']
        self.content = request_post['content']
        self.author = user
        self.voting = new_voting
        super(Question, self).save(request_post)

        list_of_tags = request_post.getlist('tags')
        for item_tag in list_of_tags:
            tags = Tag.objects.get(pk=item_tag)
            self.tag.add(tags)

    def get_vote_by(self, user_id):
        try:
            user_vote = self.author.voting.through.objects.get(user_id=user_id, voting_id=self.voting_id)
            if user_vote.value == 0:
                return 'DOWN'
            if user_vote.value == 1:
                return 'UP'
        except ObjectDoesNotExist:
            return None

    def vote_up(self, user_id):
        if self.get_vote_by(user_id):
            raise AlreadyVoted()

        self.author.voting.through.objects.create(value='1', user_id=user_id, voting_id=self.voting_id)
        self.voting.__class__.objects.filter(pk=self.voting_id).update(count_up=F('count_up') + 1)


    def vote_down(self, user_id):
        if self.get_vote_by(user_id):
            raise AlreadyVoted()

        self.author.voting.through.objects.create(value='0', user_id=user_id, voting_id=voting_id)
        self.voting.__class__.objects.filter(pk=voting_id).update(count_down=F('count_down') - 1)


class Meta:
    app_label = 'backends'
    verbose_name = 'Question'
    verbose_name_plural = 'Questions'


class AlreadyVoted(Exception):
    "Raised then users tries to vote on a question more than 1 time"
    pass


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

        print(request_post)
        self.content = request_post['content']
        self.author = user
        self.question = question
        self.voting = new_voting
        super(Answer, self).save(request_post)

    def voting_check(self, user_id, voting_id):
        if self.author.voting.through.objects.filter(user_id=user_id, voting_id=voting_id):
            return True

    def rating_up(self, user_id, voting_id):
        self.author.voting.through.objects.create(value='1', user_id=user_id, voting_id=voting_id)
        self.voting.__class__.objects.filter(pk=voting_id).update(count_up=F('count_up') + 1)

    def rating_down(self, user_id, voting_id):
        self.author.voting.through.objects.create(value='0', user_id=user_id, voting_id=voting_id)
        self.voting.__class__.objects.filter(pk=voting_id).update(count_down=F('count_down') - 1)

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

    def create(self, answer, user, request_post):
        self.content = request_post['content']
        self.author = user
        self.answer = Answer.objects.get(pk=answer)
        super(Comment, self).save(request_post)

    def __str__(self):
        return self.content


class Voting(models.Model):
    count_up = models.IntegerField(verbose_name='Count Up')
    count_down = models.IntegerField(verbose_name='Count Down')


def user_directory_path(instance, filename):
    return 'profile_picture/user_{0}/{1}'.format(instance.id, filename)


class User(AbstractUser):
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    voting = models.ManyToManyField(Voting, through='UserVoting')


class UserVoting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    value = models.IntegerField(verbose_name='Value')

    class Meta:
        unique_together = ['user', 'voting']
