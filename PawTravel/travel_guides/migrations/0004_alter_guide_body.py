# Generated by Django 4.0.3 on 2022-05-22 16:18

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_guides', '0003_remove_guide_id_alter_guide_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guide',
            name='body',
            field=tinymce.models.HTMLField(),
        ),
    ]
