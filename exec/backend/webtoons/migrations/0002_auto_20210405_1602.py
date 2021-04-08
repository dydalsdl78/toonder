# Generated by Django 3.1.7 on 2021-04-05 07:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webtoons', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='webtoon',
            name='users_webtoon',
        ),
        migrations.AddField(
            model_name='webtoon',
            name='favorite_users',
            field=models.ManyToManyField(related_name='favorite_webtoon', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='webtoon',
            name='like_users',
            field=models.ManyToManyField(related_name='like_webtoon', to=settings.AUTH_USER_MODEL),
        ),
    ]
