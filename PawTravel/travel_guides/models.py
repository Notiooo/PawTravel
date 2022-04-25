from django.db import models
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
            query_set=query_set.filter(body__icontains=keywords) | query_set.filter(title__icontains=keywords) | query_set.filter(description__icontains=keywords)
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
    slug = models.SlugField(max_length=250, unique_for_date='publish')
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
        :return: Absolute url with /YYYY/MM/DD/slug format
        '''
        return reverse('travel_guides:guide_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug
                       ])

    def save(self, *args, **kwargs):
        """
        Override of basic save function, It implements custom slug generation which will ensure It is unique
        :param args:
        :param kwargs:
        :return:
        """
        if not self.slug:

            potential_slug=slugify(self.title)
            while True:
                conflict_count=len(Guide.objects.filter(slug=potential_slug, publish__year=self.publish.year, publish__month=self.publish.month, publish__day=self.publish.day))
                if conflict_count==0:
                    self.slug=potential_slug
                    break
                else:
                    potential_slug+=str(conflict_count*-1)
        super().save(*args, **kwargs)