# Generated by Django 3.0.6 on 2021-07-31 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='upvotedownvote',
            options={'verbose_name': 'Upvote and Downvote', 'verbose_name_plural': 'Upvotes and Downvotes'},
        ),
    ]