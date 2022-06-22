from django.db import models
from django.db.models import Count, Sum
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from django.contrib.auth.models import User


class ProfileManager(models.Manager):
    def get_top_users(self):
        # sum_rating = self.annotate(answers=Sum('answer'))
        return self.annotate(answers=Count('answer')).order_by('-answers')[:12]


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, related_name='profile_related', on_delete=models.CASCADE)
    objects = ProfileManager()
    avatar = models.ImageField(upload_to='images', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class TagManager(models.Manager):
    def get_tag_by_id(self, tag_id):
        return self.filter(id=tag_id)

    def get_popular(self):
        return self.all().annotate(count=Count('question')).order_by('-count')[:20]


class Tag(models.Model):
    objects = TagManager()
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class LikeManager(models.Manager):
    def get_all(self):
        return self.all()


class Like(models.Model):
    objects = LikeManager()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    object_id = models.PositiveIntegerField()
    like_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.like_object.__str__()


class QuestionManager(models.Manager):
    def get_popular(self):
        return self.annotate(count=Count('like', distinct=True)).order_by('-count')

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
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag)
    create_date = models.DateTimeField(blank=True, auto_now=True)
    title = models.CharField(max_length=256)
    text = models.CharField(max_length=1000, blank=True)
    like = GenericRelation(Like)

    def likes(self):
        return Like.objects.filter(object_id=self.id).count()

    def __str__(self):
        return self.title

    def get_tags(self):
        return self.tags


class AnswerManager(models.Manager):
    def get_answers_by_question(self, question_id):
        return self.filter(question__id=question_id).annotate(count=Count('like')).order_by('-count')


class Answer(models.Model):
    objects = AnswerManager()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=1)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    content = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    like = GenericRelation(Like)

    def likes(self):
        return Like.objects.filter(object_id=self.id).count()

    def get_author(self):
        return self.author
