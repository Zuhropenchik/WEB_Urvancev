# Generated by Django 4.0.4 on 2022-06-19 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_question_create_date_alter_answer_question_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='answer',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
