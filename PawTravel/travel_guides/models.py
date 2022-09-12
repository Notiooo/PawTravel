from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from tinymce.models import HTMLField

from users.models import CustomUser
from comments.models import Comment
from voting.models import Vote



class GuideSearchManager(models.Manager):
    def search(self, country=None, category=None, keywords=None):
        """
        Search guides depending on defined arguments
        :param country: What country?
        :param category: What category
        :param keywords: What keywords?
        :return: Query set with guides matching above criteria
        """
        query_set = super().get_queryset().all()
        if country is not None:
            query_set = query_set.filter(country__name=country)
        if category is not None:
            query_set = query_set.filter(category__name=category)
        if keywords is not None:
            q_object = ~Q()
            for item in keywords:
                q_object &= Q(body__icontains=item) | Q(title__icontains=item) | Q(description__icontains=item)
            query_set = query_set.filter(q_object)
        query_set = query_set.filter(visible='visible')
        return query_set

    def search_by_user(self, username):
        """
        Get all guides written by specifc user
        :param username: Username
        :return:
        """
        user = CustomUser.objects.get(username=username)
        return super().get_queryset().filter(author=user, visible='visible')


class GuideCategory(models.Model):
    """Category of individual guide such as hotels"""

    name = models.CharField(max_length=100)
    icon_image = models.ImageField(blank=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    """Countries to which possibly anyone can travel"""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Guide(models.Model):
    """
    Main model of this app, It represents single travel guide
    """
    VISIBILITY = (('visible', 'Visible'), ('hidden', 'Hidden'))
    title = models.CharField(max_length=256)  #
    description = models.CharField(max_length=512)
    slug_url = models.SlugField(editable=False)
    author = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    image = models.ImageField(blank=False, null=False)
    category = models.ForeignKey(GuideCategory, on_delete=models.CASCADE, related_name='category', null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country', null=True, blank=True)
    visible = models.CharField(max_length=16, choices=VISIBILITY, default='visible')
    body = HTMLField()
    publish = models.DateTimeField(default=timezone.now)
    objects = models.Manager()  # Default manager
    search = GuideSearchManager()
    comments = GenericRelation(Comment, related_query_name='all_comments')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Generate absolute url of this object (guide)
        :return: Absolute url with slug-pk
        """
        return reverse("travel_guides:guide_detail", kwargs={'pk': self.pk, 'slug_url': self.slug_url})

    def save(self, **kwargs):
        """
        Save function provided by an additional mechanism where
        any changes should take into account slug refreshes in the url
        """
        self.slug_url = slugify(self.title)
        super(Guide, self).save(kwargs)

        @property
        def get_likes(self):
            return Vote.objects.get_score(self)['score']

        @property
        def get_votes(self):
            return Vote.objects.get_score(self)['num_votes']