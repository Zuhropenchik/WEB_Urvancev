from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import (
    Profile,
    Tag,
    Question,
    Answer,
    Like
)

import random


class Command(BaseCommand):
    GENERATION_ORDER = 50

    def handle(self, *args, **options):
        self.generate_user_and_profile()
        profiles = Profile.objects.all()
        self.generate_tags()
        tags = Tag.objects.all()
        self.generate_questions(profiles)
        questions = Question.objects.all()
        self.generate_answers(profiles, questions)
        answers = Answer.objects.all()
        self.generate_likes(profiles, questions, answers)
        for question in questions:
            for i in range(3):
                question.tags.add(random.choice(tags))

    def generate_user_and_profile(self):
        def generate_user(num):
            user_dict_repr = {
                'username': f'User{num}',
                'first_name': f'Zakhar{num}',
                'last_name': f'Urvancev{num}',
                'password': '1234',
                'email': f'{num}@example.com',
                'is_staff': False,
                'is_active': True,
                'is_superuser': False
            }
            return user_dict_repr
        profiles = []
        for i in range(self.GENERATION_ORDER):
            user = User.objects.create_user(**generate_user(i))
            p = Profile(user=user)
            p.bio = f'My name is Zakhar{i}. I want to learning!'
            profiles.append(p)
        Profile.objects.bulk_create(profiles)

    def generate_tags(self):
        tags = []
        for i in range(self.GENERATION_ORDER):
            t = Tag()
            t.title = f'tag{i}'
            tags.append(t)
        Tag.objects.bulk_create(tags)

    def generate_questions(self, profiles):
        questions = []
        for i in range(self.GENERATION_ORDER * 10):
            author = random.choice(profiles)
            q = Question()
            q.title = f'Question {i}'
            q.text = f'I dont know, help me:('
            q.author = author
            questions.append(q)
        Question.objects.bulk_create(questions)

    def generate_answers(self, profiles, questions):
        answers = []
        for i in range(self.GENERATION_ORDER * 100):
            author = random.choice(profiles)
            a = Answer()
            a.content = f'answer {i}'
            a.author = author
            a.question = random.choice(questions)
            answers.append(a)
        Answer.objects.bulk_create(answers)

    def generate_likes(self, profiles, questions, answers):
        likes = []
        for i in range(self.GENERATION_ORDER * 200):
            author = random.choice(profiles)
            answer = random.choice(answers)
            question = random.choice(questions)
            liked_object = random.choice([answer, question])
            like = Like(like_object=liked_object, user=author)
            likes.append(like)
        Like.objects.bulk_create(likes)
