import datetime
import random

import factory.fuzzy
from factory.django import DjangoModelFactory
from faker import Faker

from .models.answer import Answer
from .models.question import Question
from .models.tag import Tag
from .models.comment import Comment
from .models.user_voting import User, Voting

faker = Faker()

names = [faker.unique.first_name() for i in range(200)]

my_tag_list = [
    'Python', 'Java', 'Ruby',
    'Visual Basic', 'PHP', 'C++',
    'Kotlin', 'JavaScript', 'Swift',
    'GNU Octave', 'IDL', 'MATLAB', 'OpenCL']


# Defining a factory
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Iterator(names)
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')

    is_superuser = False
    is_staff = False
    is_active = False


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Iterator(my_tag_list)


class VotingFactory(DjangoModelFactory):
    class Meta:
        model = Voting

    count_up = factory.fuzzy.FuzzyInteger(0, 30)
    count_down = factory.fuzzy.FuzzyInteger(0, 30)


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question

    title = factory.Faker("sentence", nb_words=5, variable_nb_words=True)
    content = factory.Faker("sentence", nb_words=50, variable_nb_words=True)
    author = factory.SubFactory(UserFactory)
    created_at = datetime.datetime.now()
    tag = factory.RelatedFactory(TagFactory)
    voting = factory.SubFactory(VotingFactory)


class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = Answer

    content = factory.Faker("sentence", nb_words=20, variable_nb_words=True)
    author = factory.SubFactory(UserFactory)
    created_at = datetime.datetime.now()

    question = factory.SubFactory(QuestionFactory)
    voting = factory.SubFactory(VotingFactory)


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    content = factory.Faker("sentence", nb_words=10, variable_nb_words=True)
    author = factory.SubFactory(UserFactory)
    created_at = datetime.datetime.now()
    answer = factory.SubFactory(AnswerFactory)

