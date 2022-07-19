# Generated by Django 3.2.13 on 2022-07-19 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel_guides', '0006_auto_20220720_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guide',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='travel_guides.guidecategory'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='country', to='travel_guides.country'),
        ),
    ]
