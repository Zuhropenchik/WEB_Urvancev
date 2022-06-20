from django.core.management.base import BaseCommand, CommandError

from app.models import (
    User,
    Tag,
    Question,
    Answer,
    Like
)

import random


class Command(BaseCommand):
    GENERATION_ORDER = 1

    def handle(self, *args, **options):
        # self.generate_users()
        # self.generate_tags()
        # self.generate_questions()
        self.generate_answers()
        self.generate_likes()

    def generate_users(self):
        users = []
        for i in range(self.GENERATION_ORDER):
            u = User()
            u.username = f'User{i}'
            u.email = f'{i}@example.com'
            u.password = "123"
            users.append(u)
        User.objects.bulk_create(users)

    def generate_tags(self):
        tags = []
        for i in range(self.GENERATION_ORDER):
            t = Tag()
            t.title = f'tag{i}'
            tags.append(t)
        Tag.objects.bulk_create(tags)

    def generate_questions(self):
        questions = []
        for i in range(self.GENERATION_ORDER * 10):
            author = random.choice(User.objects.all())
            q = Question()
            q.title = f'Question {i}'
            q.text = f'I dont know, help me:('
            q.author = author
            q.save()
            q.tags.add(random.choice(Tag.objects.all()))
            questions.append(q)
        Question.objects.bulk_create(questions)

    def generate_answers(self):
        answers = []
        for i in range(self.GENERATION_ORDER * 100):
            author = random.choice(User.objects.all())
            a = Answer()
            a.text = f'answer {i}'
            a.author = author
            a.question = random.choice(Question.objects.all())
            answers.append(a)
        Answer.objects.bulk_create(answers)

    def generate_likes(self):
        for i in range(self.GENERATION_ORDER * 200):
            like = Like()
