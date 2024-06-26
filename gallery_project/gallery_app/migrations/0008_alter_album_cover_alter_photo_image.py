# Generated by Django 5.0.3 on 2024-04-07 08:42

import gallery_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery_app', '0007_alter_myuser_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.ImageField(upload_to=gallery_app.models.new_file_name),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to=gallery_app.models.new_file_name),
        ),
    ]
