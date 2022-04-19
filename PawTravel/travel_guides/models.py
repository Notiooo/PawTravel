from django.db import models
from django.urls import reverse
from django.utils import timezone
# Create your models here.


class Guide(models.Model):
    '''
    Main model of this app, It represents single travel guide
    '''
    #STATUS = () #Travel Guide status

    CATEGORY_CHOICES=(('other', 'Inne'),) #List of available categories to the user
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