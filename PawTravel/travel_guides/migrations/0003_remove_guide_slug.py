# Generated by Django 3.2.13 on 2022-05-29 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel_guides', '0002_auto_20220529_2339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guide',
            name='slug',
        ),
    ]
