# Generated by Django 4.0.4 on 2022-06-21 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_answer_likes_remove_question_likes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Profile',
        ),
    ]
