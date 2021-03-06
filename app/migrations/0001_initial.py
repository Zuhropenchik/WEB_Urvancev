# Generated by Django 4.0.4 on 2022-06-18 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Tag')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=254)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='images')),
                ('password', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('text', models.CharField(max_length=1000)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.user')),
                ('tags', models.ManyToManyField(to='app.tag')),
            ],
        ),
    ]
