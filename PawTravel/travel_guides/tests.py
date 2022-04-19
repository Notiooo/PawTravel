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

    def test_custom_save(self):
        """
        Guide model has own save method which can be used to generate unique slugs.
        This test checks if this works properly.
        """
        time=timezone.now()
        guide_one=Guide(title="Lorem Ipsum", publish=time)
        guide_one.save()
        guide_two=Guide(title="Lorem Ipsum", publish=time)
        guide_two.save()
        self.assertEqual("lorem-ipsum", guide_one.slug) #guide_one is first therefore it should not contain extra number
        self.assertEqual("lorem-ipsum-1", guide_two.slug) #guide_two is second therefore It will have 1 attached to it

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