import string
import random

from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
# Create your models here.
from django.utils.text import slugify

class GuideSearchManager(models.Manager):
    def search(self, country=None, category=None, keywords=None):
        """
        Search guides depending on defined arguments
        :param country: What country?
        :param category: What category
        :param keywords: What keywords?
        :return: Query set with guides matching above criteria
        """
        query_set=super().get_queryset().all()
        if country is not None:
            query_set=query_set.filter(country=country)
        if category is not None:
            query_set=query_set.filter(category=category)
        if keywords is not None:
            q_object = ~Q()
            for item in keywords:
                q_object &= Q(body__icontains=item) | Q(title__icontains=item) | Q(description__icontains=item)
            query_set = query_set.filter(q_object)
        return query_set

    def search_by_user(self, username):
        """
        Get all guides written by specifc user
        :param username: Username TODO: Update when user system is implemented
        :return:
        """
        return super().get_queryset().filter(author=username)


class Guide(models.Model):
    '''
    Main model of this app, It represents single travel guide
    '''
    #STATUS = () #Travel Guide status

    CATEGORY_CHOICES=(('other', 'Inne'), ('hotels', 'Hotele')) #List of available categories to the user
    COUNTRY_CHOICES=(('poland', 'Polska'),) #Countries to which travel guide can be linked
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)
    slug = models.SlugField(max_length=250, primary_key=True, unique=True, editable=True, blank=True)
    author = models.CharField(max_length=16) #Until users module is finished author will be represented only as username
    #author = models.ForeignKey() #Foreign key which links travel guide to its author
    category = models.CharField(max_length=24, choices=CATEGORY_CHOICES)
    country = models.CharField(max_length=32, choices=COUNTRY_CHOICES)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    objects = models.Manager() #Default manager
    search = GuideSearchManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        '''
        Generate absolute url of this object (guide)
        :return: Absolute url with slug-pk
        '''
        return reverse("travel_guides:guide_detail", args=[self.slug])

    def save(self, *args, **kwargs):
        """
        Custom save function. Newly created guide will get slug in title-PK format even if slug was already predefined.
        In such case slug will be overwritten.
        """
        self.slug=None
        while not self.slug:

            id = ''.join([
                "".join(random.sample(string.ascii_letters, 2)),
                "".join(random.sample(string.digits, 2)),
                "".join(random.sample(string.ascii_letters, 2)),
            ])
            newslug="{}-{}".format(slugify(self.title), id)
            if not Guide.objects.filter(pk=newslug).exists():
                self.slug = newslug

        super().save(*args, **kwargs)
