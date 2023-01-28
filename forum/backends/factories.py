import factory.fuzzy
from factory.django import DjangoModelFactory
from faker import Faker

from .models import User, Question, Tag

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

    # username = factory.LazyAttribute(
    #     lambda obj: factory.fuzzy.FuzzyChoice(names).fuzz() + str(random.randrange(1960, 2010, 1)))
    username = factory.Iterator(names)
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')

    is_superuser = False
    is_staff = False
    is_active = False


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Iterator(my_tag_list)


class VotingFactory(DjangoModelFactory):
    count_up = faker.random
    count_down = faker.random


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question

    title = factory.Faker("sentence", nb_words=5, variable_nb_words=True)
    content = factory.Faker("sentence", nb_words=50, variable_nb_words=True)
    author = factory.SubFactory(UserFactory)
    created_at = faker.date_time_this_century()
    tag = factory.SubFactory(TagFactory)
    voting = factory.SubFactory(VotingFactory)
