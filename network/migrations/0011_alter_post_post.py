# Generated by Django 4.0.1 on 2022-01-28 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_remove_user_followers_remove_user_following_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post',
            field=models.CharField(max_length=255),
        ),
    ]