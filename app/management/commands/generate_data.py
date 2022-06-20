from django.core.management.base import BaseCommand, CommandError

from app.models import (
    User,
    Tag,
    Question,
    Answer,
    Like
)

import random

GENERATION_ORDER = 10000


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.generate_users()
        self.generate_tags()
        self.generate_questions()
        self.generate_answers()

    def generate_users(self):
        for i in range(GENERATION_ORDER):
            user = User()
            user.username = f'Username{i}'
            user.email = f'{i}@live.com'
            user.password = "qwerty"

            user.save()

    def generate_tags(self):
        for i in range(GENERATION_ORDER):
            tag = Tag()
            tag.title = f'tag{i}'

            tag.save()

    def generate_questions(self):
        for i in range(GENERATION_ORDER * 10):
            author = random.choice(User.objects.all())
            q = Question()
            q.title = f'Question {i}'
            q.text = f'How to do the {i} task?'
            q.author = author
            q.save()
            q.tags.add(random.choice(Tag.objects.all()))

    def generate_answers(self):
        author = random.choice(User.objects.all())
        for i in range(GENERATION_ORDER * 100):
            answer = Answer()
            answer.text = f'answer {i}'
            answer.author = author
            answer.question = random.choice(Question.objects.all())
            answer.save()

    def generate_likes(self):
        for i in range(GENERATION_ORDER * 200):
            like = Like()
