from django.test import TestCase
from .models import Guide
from django.utils import timezone

# Create your tests here.
class GuideModelTests(TestCase):


    def test_absolute_url(self):
        """
        Checks if absolute url is generated properly with given slug
        """
        slug="lorem-ipsum"
        guide=Guide(slug=slug)
        date=timezone.now()
        url=guide.get_absolute_url()
        expected="/guide/{:04d}/{:02d}/{:02d}/{}/".format(date.year, date.month, date.day, slug)
        self.assertEqual(expected, url)