# Generated by Django 4.2.7 on 2023-11-10 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0002_article_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='catgory',
            new_name='category',
        ),
    ]