import random

from django.core.management.base import BaseCommand
from django.db import transaction

from ...factories import (
    UserFactory,
    TagFactory, QuestionFactory, AnswerFactory, CommentFactory)
from ...models import User, Tag, Question, Voting, Answer, Comment

NUM_USERS = 20
NUM_TAGS = 10

NUM_QUESTIONS = 20
NUM_ANSWERS = 30
NUM_COMMENTS = 30

QUESTION_TAG_MAX = 3


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        Question.tag.through.objects.all().delete()
        models = [Comment, Answer, Voting, Question, Tag, User]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        people = []
        for x in range(NUM_USERS):
            person = UserFactory()
            people.append(person)

        tags = []
        for _ in range(NUM_TAGS):
            tag = TagFactory()
            tags.append(tag)

        questions = []
        for _ in range(NUM_QUESTIONS):
            question = QuestionFactory()
            tag = random.choices(
                tags,
                k=QUESTION_TAG_MAX
            )
            question.tag.add(*tag)
            questions.append(question)

        answers = []
        for _ in range(NUM_ANSWERS):
            question = random.choice(questions)
            answer = AnswerFactory(question=question, is_useful=random.choice([True, False]))
            answers.append(answer)

        comments = []
        for _ in range(NUM_COMMENTS):
            answer = random.choice(answers)
            comment = CommentFactory(answer=answer)
            comments.append(comment)
        self.stdout.write("New data successfully сreated")
