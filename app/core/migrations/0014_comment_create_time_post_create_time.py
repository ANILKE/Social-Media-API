# Generated by Django 4.0.10 on 2024-03-08 06:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_rename_related_post_id_comment_related_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='post',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
