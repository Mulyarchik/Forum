import datetime

from django.test import TestCase

from .models.question import Question
from .models.tag import Tag
from .models.user_voting import User, Voting


class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        tag = Tag.objects.create(name='Python')
        user = User.objects.create(first_name='Test1', last_name='Test2', username='test1', email='test@test.test',
                                   password='vlad53sd2$$$')
        voting = Voting.objects.create(count_up=-1, count_down=+5)
        question = Question.objects.create(title='how to enable django support in pycharm',
                                           content='guys urgently need help. how to enable django support in pycharm????',
                                           created_at=datetime.datetime.now(),
                                           author=user,
                                           voting=voting)
        question.tag.add(tag.id)

    def test_total(self):
        question = Question.objects.get(id=1)
        voting = Voting.objects.get(id=question.voting_id)
        self.assertEquals(question.total, voting.count_up + voting.count_down)

    def test_get_absolute_url(self):
        question = Question.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(question.get_absolute_url(), "/questions/1/")
