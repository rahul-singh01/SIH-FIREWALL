# Generated by Django 5.1 on 2024-09-09 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='policy',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
