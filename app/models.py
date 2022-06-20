from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now


class UserManager(models.Manager):
    def get_popular(self):
        return self.filter(likes__gt=10)

    def get_user_by_answer(self, question_id):
        return self.filter(id)


class User(models.Model):
    objects = UserManager()
    username = models.CharField(max_length=256)
    email = models.EmailField()
    avatar = models.ImageField(upload_to='images', null=True, blank=True)
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.username


class TagManager(models.Manager):
    def get_tag_by_id(self, tag_id):
        return self.filter(id=tag_id)


class Tag(models.Model):
    objects = TagManager()
    title = models.CharField(max_length=50, verbose_name="Tag")

    def __str__(self):
        return self.title


class QuestionManager(models.Manager):
    def get_popular(self):
        return sorted(self.filter(likes__gt=10), key=lambda question: question.likes, reverse=True)

    def get_recent(self):
        return self.filter(created_date__gt=now())

    def get_question_by_id(self, question_id):
        return self.filter(id=question_id)

    def get_questions_by_user_id(self, user_id):
        return self.filter(author__user=user_id)

    def get_questions_by_tag_title(self, title):
        return self.filter(tags__title=title)

    def get_question_answers(self, question_id: int):
        return self.filter(answers__author__questions=question_id)


class Question(models.Model):
    objects = QuestionManager()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag)
    create_date = models.DateTimeField(blank=True, auto_now=True)
    title = models.CharField(max_length=256)
    text = models.CharField(max_length=1000, blank=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_tags(self):
        return self.tags


class AnswerManager(models.Manager):

    def get_answers_by_question(self, question_id):
        return self.filter(question__id=question_id)


class Answer(models.Model):
    objects = AnswerManager()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)

    def get_author(self):
        return self.author


class LikeManager(models.Manager):
    def get_all(self):
        return self.all()


class Like(models.Model):
    objects = LikeManager()
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    object_id = models.PositiveIntegerField()
    like_object = GenericForeignKey('content_type', 'object_id')
