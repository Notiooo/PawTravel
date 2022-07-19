# Generated by Django 3.2.13 on 2022-06-02 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('title', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=1024)),
                ('slug', models.SlugField(blank=True, max_length=250, primary_key=True, serialize=False, unique=True)),
                ('category', models.CharField(choices=[('other', 'Other'), ('hotels', 'Hotels')], max_length=24)),
                ('country', models.CharField(choices=[('poland', 'Poland')], max_length=32)),
                ('visible', models.CharField(choices=[('visible', 'Visible'), ('hidden', 'Hidden')], default='visible', max_length=16)),
                ('body', tinymce.models.HTMLField()),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
    ]
