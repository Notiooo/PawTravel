from django.test import TestCase
from django.test.client import RequestFactory, Client

from .models import Guide
from django.utils import timezone
from users.models import CustomUser
from .views import GuideFormView, GuideVoteView
import json

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

        self.assertNotEqual(guide_one.slug, guide_two.slug)

    def test_custom_save_other_guide_collision(self):
        """
        If we add '1' to article's slug it may collide with article which had this '1' in its title
        """
        time = timezone.now()
        guide_special = Guide(title="Lorem Ipsum 1", publish=time, author=self.author)
        guide_special.save()
        guide_one = Guide(title="Lorem Ipsum", publish=time, author=self.author)
        guide_one.save()
        guide_two = Guide(title="Lorem Ipsum", publish=time, author=self.author)
        guide_two.save()
        self.assertNotEqual(guide_two.slug, guide_special.slug)


class GuidesViewTests(TestCase):
    """
    Test class responsible for testing views
    """
    def setUp(self) -> None:

        self.author=CustomUser(username="TestUser")
        self.author.save()
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
        Guide(author=self.author, category="hotels", description="It is test Lorem ipsum").save()
        Guide(author=self.author, country="poland", body="It is only test").save()
        Guide(author=self.author_two, title="Lorem test ipsum").save()
        Guide(author=self.author_two,  country="poland", category="hotels", body="message").save()

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
        self.author=CustomUser(username="TestUser", email="test_email@test.com")
        self.author.save()
        self.guide=Guide(title="Test guide", author=self.author)
        self.guide.save()
        self.guide_two=Guide(title="Test guide", author=self.author, visible='Hidden')
        self.guide_two.save()
        self.guide_three=Guide(title="Test guide", author=self.author)
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

class VotingSystemTests(TestCase):
    """
    This class is responsible for testing implementation of voting system
    """
    def setUp(self):
        """
        Preparing single guide and two user accounts
        """
        self.user_one=CustomUser(username="TestUser", email="test_email@test.com")
        self.user_one.save()
        self.guide=Guide(title="Test guide", author=self.user_one)
        self.guide.save()


    def test_vote_response(self):
        """
        Checks if voting paths return correct code (200)
        """
        url=self.guide.get_absolute_url()
        id=url.split("/")[-2]
        c=Client(username="TestUser", email="test_email_two@test.com")
        c.login(username="TestUser", email="test_email_two@test.com")
        for option in ["like", "dislike"]:
            vote_url="/guides/vote/{}/{}".format(id, option)
            response=c.post(vote_url)
            self.assertEqual(response.status_code, 200, "Option {} returned code {}".format(option, response.status_code))

    def test_vote_up_amount(self):
        """
        Checks if system counts up votes correctly
        """
        url = self.guide.get_absolute_url()
        id = url.split("/")[-2]
        vote_url = "/guides/vote/{}/like".format(id)
        view=GuideVoteView
        #User 1 voting up
        factory = RequestFactory()
        request = factory.post(vote_url)
        request.user = CustomUser.objects.create(username='testuser', email="test@test.com")
        response=view.post(self=view, request=request, slug=id, mode="like")
        json_response=json.loads(response.content.decode())
        self.assertEqual(json_response["likes"], 1)
        self.assertEqual(json_response["num_votes"], 1)
        #User 2 voting up
        request = factory.post(vote_url)
        request.user = CustomUser.objects.create(username='testuser2', email="test2@test.com")
        view = GuideVoteView
        response = view.post(self=view, request=request, slug=id, mode="like")
        json_response=json.loads(response.content.decode())
        self.assertEqual(json_response["likes"], 2)
        self.assertEqual(json_response["num_votes"], 2)

    def test_vote_down(self):
        """
        Checks if system counts up votes correctly
        """
        url = self.guide.get_absolute_url()
        id = url.split("/")[-2]
        vote_url = "/guides/vote/{}/dislike".format(id)
        view = GuideVoteView
        # User 1 voting down
        factory = RequestFactory()
        request = factory.post(vote_url)
        request.user = CustomUser.objects.create(username='testuser', email="test@test.com")
        response = view.post(self=view, request=request, slug=id, mode="dislike")
        json_response = json.loads(response.content.decode())
        self.assertEqual(json_response["likes"], -1)
        self.assertEqual(json_response["num_votes"], 1)
        # User 2 voting down
        request = factory.post(vote_url)
        request.user = CustomUser.objects.create(username='testuser2', email="test2@test.com")
        view = GuideVoteView
        response = view.post(self=view, request=request, slug=id, mode="dislike")
        json_response = json.loads(response.content.decode())
        self.assertEqual(json_response["likes"], -2)
        self.assertEqual(json_response["num_votes"], 2)

    def test_change_vote(self):
        """
        Checks if changing vote works as intended
        """
        url = self.guide.get_absolute_url()
        id = url.split("/")[-2]
        vote_url = "/guides/vote/{}/dislike".format(id)
        view = GuideVoteView
        # User 1 voting down
        factory = RequestFactory()
        request = factory.post(vote_url)
        request.user = CustomUser.objects.create(username='testuser', email="test@test.com")
        response = view.post(self=view, request=request, slug=id, mode="dislike")
        json_response = json.loads(response.content.decode())
        self.assertEqual(json_response["likes"], -1)
        self.assertEqual(json_response["num_votes"], 1)
        response = view.post(self=view, request=request, slug=id, mode="like")
        json_response = json.loads(response.content.decode())
        self.assertEqual(json_response["likes"], 1)
        self.assertEqual(json_response["num_votes"], 1)