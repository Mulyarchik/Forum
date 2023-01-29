from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction

VOTE_UP = 1
VOTE_DOWN = 0
VOTE_UP_COUNTER_VALUE = +1
VOTE_DOWN_COUNTER_VALUE = -1


class Voting(models.Model):
    count_up = models.IntegerField(verbose_name='Count Up')
    count_down = models.IntegerField(verbose_name='Count Down')

    def get_vote_by(self, user_id):
        try:
            user_vote = UserVoting.objects.get(voting_id=self.id, user_id=user_id)
            if user_vote.value == 0:
                return 'DOWN'
            if user_vote.value == 1:
                return 'UP'
        except ObjectDoesNotExist:
            return None

    @transaction.atomic
    def vote_up(self, user_id):
        if self.get_vote_by(user_id):
            raise AlreadyVoted()

        self.uservoting_set.create(value=VOTE_UP, user_id=user_id)
        self.count_up += 1
        self.save()

    @transaction.atomic
    def vote_down(self, user_id):
        if self.get_vote_by(user_id):
            raise AlreadyVoted()

        self.uservoting_set.create(value=VOTE_DOWN, user_id=user_id)
        self.count_up -= 1
        self.save()


class AlreadyVoted(Exception):
    "Raised then users tries to vote on a question more than 1 time"
    pass


def user_directory_path(instance, filename):
    return 'profile_picture/user_{0}/{1}'.format(instance.id, filename)


class User(AbstractUser):
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    voting = models.ManyToManyField(Voting, through='UserVoting')


class UserVoting(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    value = models.IntegerField(verbose_name='Value')

    class Meta:
        unique_together = ['user', 'voting']

    def adding_vote(self, value, user_id):
        UserVoting.objects.create(value=value, user_id=user_id, voting_id=self.id)
