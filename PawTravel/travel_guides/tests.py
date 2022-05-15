from django.test import TestCase
from django.urls import reverse

from .models import Guide
from django.utils import timezone

# Create your tests here.
class GuideModelTests(TestCase):
    """
    Test class responsible for travel_guides model testing
    """

    def test_custom_save(self):
        """
        Guide model has own save method which can be used to generate unique slugs.
        This test checks if this works properly.
        """
        guide_one=Guide(title="Lorem Ipsum")
        guide_one.save()
        guide_two=Guide(title="Lorem Ipsum")
        guide_two.save()

        self.assertNotEqual(guide_one.slug, guide_two.slug)

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


class GuidesViewTests(TestCase):
    """
    Test class responsible for testing views
    """
    def setUp(self) -> None:
        self.author="Testuser"
        self.guide=Guide(title="Test guide", author=self.author)
        self.guide.save()


    def test_guide_list(self):
        """
        Checks if travel_guides list returns correct code (200)
        """
        resp=self.client.get("/guides/list/")
        self.assertEqual(resp.status_code, 200)

    def test_guide_detail(self):
        """
        Checks if travel_guides page returns correct code (200)
        """
        resp=self.client.get(self.guide.get_absolute_url())

        self.assertEqual(resp.status_code, 200, self.guide.get_absolute_url())

    def test_user_guide_list(self):
        """
        Checks if list of specific user guides returns correct code (200)
        """
        resp=self.client.get("/guides/user/"+self.author+"/")

        self.assertEqual(resp.status_code, 200)


class GuideSearchTests(TestCase):
    """
    Test class responsible for testing custom Manager for Guide model
    """
    def setUp(self):
        Guide(author="lorem", category="hotels", description="It is test Lorem ipsum").save()
        Guide(author="ipsum", country="poland", body="It is only test").save()
        Guide(author="lorem", title="Lorem test ipsum").save()
        Guide(author="ipsum",  country="poland", category="hotels", body="message").save()

    def test_user_search(self):
        """
        Checks if search_by_user method returns correct amount of guides
        """
        query_set=Guide.search.search_by_user("lorem")
        self.assertEqual(len(query_set), 2)

    def test_one_element_search(self):
        """
        Checks if searching with single works as intended,
        """
        self.assertEqual(len(Guide.search.search(category="hotels")), 2)
        self.assertEqual(len(Guide.search.search(country="poland")), 2)
        self.assertEqual(len(Guide.search.search(keywords=["test"])), 3)

    def test_two_element_search(self):
        """
        Checks if searching with two elements works as intended.
        """

        self.assertEqual(len(Guide.search.search(category="hotels", keywords=["test"])), 1)
        self.assertEqual(len(Guide.search.search(country="poland", keywords=["test"])), 1)
        self.assertEqual(len(Guide.search.search(country="poland", category="hotels")), 1)
        self.assertEqual(len(Guide.search.search(keywords=["test", "lorem"])), 2)

    def test_three_element_search(self):
        """
        Checks if searching with three elements works as intended.
        """

        self.assertEqual(len(Guide.search.search(country="poland", category="hotels", keywords=["message"])), 1)
        self.assertEqual(len(Guide.search.search(keywords=["test", "lorem", "ipsum"])), 2)