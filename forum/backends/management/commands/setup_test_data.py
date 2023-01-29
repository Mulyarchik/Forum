import random

from django.core.management.base import BaseCommand
from django.db import transaction

from ...factories import (
    UserFactory,
    TagFactory, QuestionFactory, VotingFactory, )
from ...models import User, Tag

NUM_USERS = 20
NUM_TAGS = 10

NUM_QUESTIONS = 20
NUM_VOTING = 20

QUESTION_TAG = 7
QUESTION_VOTING = 1


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [User, Tag]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")
        # Create all the users
        # people = []
        # for x in range(NUM_USERS):
        #     person = UserFactory()
        #     people.append(person)

        tags = []
        for _ in range(NUM_VOTING):
            tag = TagFactory()
            tags.append(tag)

        # votings = []
        # for _ in range(NUM_TAGS):
        #     voting = VotingFactory()
        #     votings.append(voting)
        #
        # for _ in range(NUM_QUESTIONS):
        #     author = random.choice(people)
        #     question = QuestionFactory()
        #     tag = random.choices(
        #         tags,
        #         k=QUESTION_TAG
        #     )
        #     question.tag.add(*tag)
        #
        #     voting = random.choices(
        #         votings,
        #         k=QUESTION_VOTING
        #     )
        #     question.voting.add(*voting)
