# Generated by Django 4.2.7 on 2023-11-10 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='slug',
            field=models.SlugField(allow_unicode=True, auto_created=True, default=None, unique=True),
        ),
    ]
