# Generated by Django 5.0.3 on 2024-04-06 12:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery_app', '0004_remove_album_anonymous_album_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
