# Generated by Django 4.0.3 on 2022-05-01 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0003_offer_shortcontent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='shortContent',
            field=models.TextField(blank=True, max_length=300),
        ),
    ]
