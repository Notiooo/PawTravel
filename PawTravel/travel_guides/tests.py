import tempfile

from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from .models import Guide, GuideCategory, Country
from parameterized import parameterized
from users.models import CustomUser
from .views import GuideFormView

# Create your tests here.
class GuideModelTests(TestCase):
    """
    Test class responsible for travel_guides model testing
    """
    def setUp(self) -> None:
        self.author=CustomUser(username="TestUser", email="test_email@test.com")
        self.author.save()

    def test_custom_save(self):
        """
        Guide model has own save method which can be used to generate unique slugs.
        This test checks if this works properly.
        """
        guide_one=Guide(title="Lorem Ipsum", author=self.author)
        guide_one.save()
        guide_two=Guide(title="Lorem Ipsum", author=self.author)
        guide_two.save()

        self.assertEqual(guide_one.slug_url, "lorem-ipsum")
        self.assertEqual(guide_one.pk, 1)
        self.assertEqual(guide_two.slug_url, "lorem-ipsum")
        self.assertEqual(guide_two.pk, 2)


class GuidesViewTests(TestCase):
    """
    Test class responsible for testing views
    """
    def setUp(self) -> None:
        self.author = CustomUser(username="TestUser")
        self.author.save()
        self.category = GuideCategory(name="Test Category")
        self.category.save()
        self.country = Country(name="Test Country")
        self.country.save()
        self.guide = Guide(title="Test guide", author=self.author, category=self.category, country=self.country,
                           image=tempfile.NamedTemporaryFile(suffix=".jpg").name)
        self.guide.save()

    @parameterized.expand([
        ('/guides/1/', 302),
        ('/guides/slug-url-9-1', 301),
        ('/guides/slug-url--1', 301),
        ('/guides/slug-url-9-1/', 302),
        ('/guides/slug-url--1/', 302),
        ('/guides/1', 301),
        ('/guides/test-guide-1/', 200),
    ])
    def test_view_status_code(self, test_input, status_code):
        """
        Test to verify the correctness of the status codes of each url
        """
        response = self.client.get(test_input)
        self.assertEqual(response.status_code, status_code)

    @parameterized.expand([
        '/guides/1/',
        '/guides/slug-url-9-1',
        '/guides/slug-url--1',
        '/guides/slug-url-9-1/',
        '/guides/slug-url--1/',
        "/guides/1",
    ])
    def test_view_by_name_and_url_are_the_same(self, test_input):
        """
        Test to verify the correctness of the redirection of each url
        """
        response_name = self.client.get(reverse('travel_guides:guide_detail', kwargs={'pk': 1}), follow=True)
        response_url = self.client.get(test_input, follow=True)
        self.assertEqual(response_name.redirect_chain[-1], response_url.redirect_chain[-1])
        self.assertEqual(response_name.status_code, 200)
        self.assertEqual(response_url.status_code, 200)

    def test_view_by_name_status_code(self):
        """
        Test to verify that with the correct pk there will be a redirect
        """
        response = self.client.get(reverse('travel_guides:guide_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

    def test_view_by_name_follow(self):
        """
        Test to verify that with the correct pk there will be a redirect to the correct page
        """
        response = self.client.get(reverse('travel_guides:guide_detail', kwargs={'pk': 1}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1], ('/guides/test-guide-1/', 302))

    def test_view_by_name_with_wrong_slug_status_code(self):
        """
        Test to verify that with correct pk but wrong slug will redirect
        """
        response = self.client.get(reverse('travel_guides:guide_detail', kwargs={'pk': 1, 'slug_url': 'any-slug-url'}))
        self.assertEqual(response.status_code, 302)

    def test_view_by_name_with_wrong_slug_follow(self):
        """
        Test to verify that with correct pk but wrong slug will redirect to correct page
        """
        response = self.client.get(reverse('travel_guides:guide_detail', kwargs={'pk': 1, 'slug_url': 'any-slug-url'}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1], ('/guides/test-guide-1/', 302))

    def test_view_by_name_with_correct_slug(self):
        """
        Test to verify that with a valid slug and pk given to url there should be no redirection
        """
        response = self.client.get(reverse('travel_guides:guide_detail', kwargs={'pk': 1, 'slug_url': 'test-guide'}))
        self.assertEqual(response.status_code, 200)

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
        resp=self.client.get("/guides/user/"+self.author.username+"/")

        self.assertEqual(resp.status_code, 200)

    def test_guide_add_form(self):
        """
        Checks if guide creation form is protected from non logged users
        """
        resp=self.client.get("/guides/add")
        self.assertEqual(resp.status_code, 301, "User should not be able to access this page if not logged")
        factory = RequestFactory()
        request = factory.get('/guides/add')
        request.user = CustomUser.objects.create(username='testuser', email="test@test.com")
        response = GuideFormView.as_view()(request)
        self.assertEqual(response.status_code, 200, "User should be able to access this page if logged")


class GuideSearchTests(TestCase):
    """
    Test class responsible for testing custom Manager for Guide model
    """
    def setUp(self):
        self.author=CustomUser(username="TestUser", email="test_email@test.com")
        self.author.save()
        self.author_two=CustomUser(username="TestUser2", email="test_email_two@test.com")
        self.author_two.save()
        self.category = GuideCategory(name="hotels")
        self.category.save()
        self.country = Country(name="poland")
        self.country.save()
        Guide(author=self.author, category=self.category, description="It is test Lorem ipsum").save()
        Guide(author=self.author, country=self.country, body="It is only test").save()
        Guide(author=self.author_two, title="Lorem test ipsum").save()
        Guide(author=self.author_two,  country=self.country, category=self.category, body="message").save()

    def test_user_search(self):
        """
        Checks if search_by_user method returns correct amount of guides
        """
        query_set=Guide.search.search_by_user("TestUser")
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


class VisibilityTest(TestCase):
    """
    This class tests if visibility settings works correctly
    """
    def setUp(self):
        self.category = GuideCategory(name="Test Category")
        self.category.save()
        self.country = Country(name="Test Country")
        self.country.save()
        self.author = CustomUser(username="TestUser", email="test_email@test.com")
        self.author.save()
        self.guide = Guide(title="Test guide", author=self.author, category=self.category, country=self.country)
        self.guide.save()
        self.guide_two = Guide(title="Test guide", author=self.author,
                               visible='Hidden', category=self.category, country=self.country)
        self.guide_two.save()
        self.guide_three = Guide(title="Test guide", author=self.author, category=self.category, country=self.country)
        self.guide_three.save()

    def test_list_with_hidden_article_default(self):
        """
        Checks if guide list omits hidden articles
        """
        self.assertEqual(len(Guide.search.search()), 2)

    def test_list_with_hidden_article_user(self):
        """
        Checks if guide list omits hidden articles, however we search by author
        """
        self.assertEqual(len(Guide.search.search_by_user(self.author.username)), 2)

    def test_hidden_guide_detail(self):
        """
        Checks if server returns code 404 if someone tries to access hidden article
        """
        resp=self.client.get(self.guide_two.get_absolute_url())
        self.assertEqual(resp.status_code, 404)
