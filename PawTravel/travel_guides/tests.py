from django.test import TestCase
from .models import Guide
from django.utils import timezone

# Create your tests here.
class GuideModelTests(TestCase):
    """
    Test class responsible for guide model testing
    """

    def test_absolute_url(self):
        """
        Checks if absolute url is generated properly with given slug
        """
        slug="lorem-ipsum"
        guide=Guide(slug=slug)
        date=timezone.now()
        url=guide.get_absolute_url()
        expected="/guides/{:04d}/{:02d}/{:02d}/{}/".format(date.year, date.month, date.day, slug)
        self.assertEqual(expected, url)

class GuidesViewTests(TestCase):
    """
    Test class responsible for testing views
    """
    def setUp(self):
        """
        Create single guide with defined slug and author
        """
        self.slug="losem-ipsum"
        self.author="admin"
        Guide.objects.create(slug=self.slug, author=self.author)


    def test_guide_list(self):
        """
        Checks if guide list returns correct code (200)
        """
        resp=self.client.get("/guides/")
        self.assertEqual(resp.status_code, 200)

    def test_guide_detail(self):
        """
        Checks if guide page returns correct code (200)
        """
        guides=Guide.objects.get(slug=self.slug)
        resp=self.client.get(guides.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

    def test_user_guide_list(self):
        """
        Checks if list of specific user guides returns correct code (200)
        """
        resp=self.client.get("/guides/user/"+self.author+"/")

        self.assertEqual(resp.status_code, 200)