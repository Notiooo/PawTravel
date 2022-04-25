from django.test import TestCase
from django.urls import reverse

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

    def test_custom_save_other_guide_collision(self):
        """
        If we add '1' to article's slug it may collide with article which had this '1' in its title
        """
        time = timezone.now()
        guide_special = Guide(title="Lorem Ipsum 1", publish=time)
        guide_special.save()
        guide_one = Guide(title="Lorem Ipsum", publish=time)
        guide_one.save()
        guide_two = Guide(title="Lorem Ipsum", publish=time)
        guide_two.save()
        self.assertNotEqual(guide_two.slug, guide_special.slug)

    def test_same_slug_different_date(self):
        """
        If two articles have the same title they can still get same slug if they were posted on different dates
        """
        time = timezone.now()
        guide_one = Guide(title="Lorem Ipsum", publish=time)
        guide_one.save()
        time=time.replace(month=time.month-1)
        guide_two = Guide(title="Lorem Ipsum", publish=time)
        guide_two.save()
        self.assertEqual(guide_one.slug, guide_two.slug)


class GuidesViewTests(TestCase):
    """
    Test class responsible for testing views
    """
    def setUp(self):
        """
        Create single guide with defined slug and author
        """
        self.slug="lorem-ipsum"
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

    def test_pagination_out_of_range(self):
        """
        Checks if pagination returns last page if out of range
        """
        response = self.client.get(reverse('travel_guides:guide_list'), {'guides': Guide.objects.all(), 'page': 999})
        self.assertEqual(response.context['guides'].number, 1)

    def test_pagination_not_an_integer(self):
        """
        Checks if pagination works correctly if page number is not an integer
        """
        response = self.client.get(reverse('travel_guides:guide_list'), {'guides': Guide.objects.all(), 'page': "test"})
        self.assertEqual(response.context['guides'].number, 1)