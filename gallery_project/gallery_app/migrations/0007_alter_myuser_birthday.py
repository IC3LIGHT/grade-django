# Generated by Django 5.0.3 on 2024-04-06 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery_app', '0006_remove_myuser_is_active_remove_myuser_is_admin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='birthday',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
