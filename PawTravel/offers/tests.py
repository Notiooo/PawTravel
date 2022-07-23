import datetime
import json
import tempfile

from django.test import TestCase
from django.urls import reverse
from offers.models import Offer, OfferCategory
from parameterized import parameterized_class, parameterized
from users.models import CustomUser
from pathlib import Path
from django.test import Client
import json
from django.test.client import RequestFactory
from .views import OfferDetailView, OfferVoteView


class DetailOfferViewTestCase(TestCase):
    """Tests for correct displaying of a specific single offer"""

    def setUp(self):
        """Inserts the necessary test objects into the database"""

        self.mock_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.current_time = datetime.datetime.now()
        user = CustomUser.objects.create(username='user1')
        OfferCategory.objects.create(name="TestCategory")
        Offer.objects.create(
            title="TestTitle",
            short_content="Example short content",
            content="<b>Styled content</b>",
            category=OfferCategory.objects.get(id=1),
            image=self.mock_file,
            offer_ends=datetime.datetime(2022, 12, 13, 14, 57, 11, 342380),
            author=user,
            original_price=1999.99,
            offer_price=989.99,
            link="http://google.com"
        )

    @parameterized.expand([
        ('/offers/1/', 302),
        ('/offers/slug-url-9-1', 301),
        ('/offers/slug-url--1', 301),
        ('/offers/slug-url-9-1/', 302),
        ('/offers/slug-url--1/', 302),
        ('/offers/1', 301),
        ('/offers/testtitle-1/', 200),
    ])
    def test_view_status_code(self, test_input, status_code):
        response = self.client.get(test_input)
        self.assertEqual(response.status_code, status_code)

    @parameterized.expand([
        '/offers/1/',
        '/offers/slug-url-9-1',
        '/offers/slug-url--1',
        '/offers/slug-url-9-1/',
        '/offers/slug-url--1/',
        "/offers/1",
    ])
    def test_view_by_name_and_url_are_the_same(self, test_input):
        response_name = self.client.get(reverse('offer', kwargs={'pk': 1}), follow=True)
        response_url = self.client.get(test_input, follow=True)
        self.assertEqual(response_name.redirect_chain[-1], response_url.redirect_chain[-1])
        self.assertEqual(response_name.status_code, 200)
        self.assertEqual(response_url.status_code, 200)

    def test_view_by_name_status_code(self):
        response = self.client.get(reverse('offer', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

    def test_view_by_name_follow(self):
        response = self.client.get(reverse('offer', kwargs={'pk': 1}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1], ('/offers/testtitle-1/', 302))

    def test_view_by_name_with_wrong_slug_status_code(self):
        response = self.client.get(reverse('offer', kwargs={'pk': 1, 'slug_url': 'any-slug-url'}))
        self.assertEqual(response.status_code, 302)

    def test_view_by_name_with_wrong_slug_follow(self):
        response = self.client.get(reverse('offer', kwargs={'pk': 1, 'slug_url': 'any-slug-url'}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1], ('/offers/testtitle-1/', 302))

    def test_view_by_name_with_correct_slug(self):
        response = self.client.get(reverse('offer', kwargs={'pk': 1, 'slug_url': 'testtitle'}))
        self.assertEqual(response.status_code, 200)

    def test_view_correct_template(self):
        response = self.client.get(reverse('offer', kwargs={'pk': 1, 'slug_url': 'testtitle'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/detailed_offer.html')

    def test_view_correct_title(self):
        response = self.client.get('/offers/testtitle-1/')
        self.assertContains(response, "TestTitle")

    def test_view_correct_short_content(self):
        response = self.client.get('/offers/testtitle-1/')
        self.assertContains(response, "Example short content")

    def test_view_correct_content(self):
        response = self.client.get('/offers/testtitle-1/')
        self.assertContains(response, "<b>Styled content</b>")

    def test_view_correct_category(self):
        response = self.client.get('/offers/testtitle-1/')
        self.assertContains(response, "TestCategory")

    def test_view_correct_image(self):
        response = self.client.get('/offers/testtitle-1/')
        self.assertContains(response, Path(self.mock_file).name)

    def test_view_correct_date_posted(self):
        response = self.client.get('/offers/testtitle-1/')
        self.assertContains(response, f'{self.current_time.year}')
        self.assertContains(response, f'{self.current_time.day}')
        self.assertContains(response, f'{self.current_time.month}')

    def test_view_correct_offer_ends(self):
        response = self.client.get('/offers/testtitle-1/')
        self.assertContains(response, "2022")
        self.assertContains(response, "12")
        self.assertContains(response, "13")
        self.assertContains(response, "14")
        self.assertContains(response, "57")

    def test_view_correct_author(self):
        response = self.client.get('/offers/testtitle-1/')
        self.assertContains(response, "user1")

    def test_view_correct_original_price(self):
        response = self.client.get('/offers/testtitle-1/')
        self.assertContains(response, "1999.99")

    def test_view_correct_offer_price(self):
        response = self.client.get('/offers/testtitle-1/')
        self.assertContains(response, "989.99")

    def test_view_correct_link(self):
        response = self.client.get('/offers/testtitle-1/')
        self.assertContains(response, "http://google.com")


class DetailOfferTestCase(TestCase):
    """Tests that check the model itself rather than the view itself"""

    def setUp(self):
        """Inserts the necessary test objects into the database"""
        user = CustomUser.objects.create(username='user1')
        OfferCategory.objects.create(name="TestCategory")
        Offer.objects.create(
            title="TestTitle",
            short_content="Example short content",
            content="<b>Styled content</b>",
            category=OfferCategory.objects.get(id=1),
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            offer_ends=datetime.datetime(2022, 12, 13, 14, 57, 11, 342380),
            author=user,
            original_price=1999.99,
            offer_price=989.99,
            link="http://google.com"
        )

    def test_correct_string_display(self):
        offer = Offer.objects.get(id=1)
        expected_offer_name = f'{offer.title}'
        self.assertEqual(expected_offer_name, 'TestTitle')

    def test_correct_offer_content(self):
        offer = Offer.objects.get(id=1)
        self.assertEqual(f'{offer.title}', "TestTitle")
        self.assertEqual(f'{offer.short_content}', "Example short content")
        self.assertEqual(f'{offer.category}', "TestCategory")
        self.assertEqual(f'{offer.image}'[-4:], ".jpg")
        self.assertEqual(f'{offer.offer_ends}', "2022-12-13 14:57:11.342380+00:00")
        self.assertEqual(f'{offer.author}', "user1")
        self.assertEqual(f'{offer.original_price}', "1999.99")
        self.assertEqual(f'{offer.offer_price}', "989.99")
        self.assertEqual(f'{offer.link}', "http://google.com")

    def test_get_absolute_url(self):
        offer = Offer.objects.get(id=1)
        self.assertEquals(offer.get_absolute_url(), '/offers/testtitle-1/')

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
        OfferCategory.objects.create(name="TestCategory")

        Offer.objects.create(
            title="TestTitle",
            short_content="Example short content",
            content="<b>Styled content</b>",
            category=OfferCategory.objects.get(id=1),
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            offer_ends=datetime.datetime(2022, 12, 13, 14, 57, 11, 342380),
            author=self.user_one,
            original_price=1999.99,
            offer_price=989.99,
            link="http://google.com"
        )
        self.offer = Offer.objects.get(id=1)



    def test_vote_response(self):
        """
        Checks if voting paths return correct code (200)
        """
        id=self.offer.id
        c=Client(username="TestUser", email="test_email_two@test.com")
        c.login(username="TestUser", email="test_email_two@test.com")
        for option in ["like", "dislike"]:
            vote_url="/offers/vote/{}/{}".format(id, option)
            response=c.post(vote_url)
            self.assertEqual(response.status_code, 200, "Option {} returned code {}".format(option, response.status_code))

    def test_vote_up_amount(self):
        """
        Checks if system counts up votes correctly
        """
        id = self.offer.id
        vote_url = "/offers/vote/{}/like".format(id)
        view=OfferVoteView
        #User 1 voting up
        factory = RequestFactory()
        request = factory.post(vote_url)
        request.user = CustomUser.objects.create(username='testuser', email="test@test.com")
        response=view.post(self=view, request=request, pk=id, mode="like")
        json_response=json.loads(response.content.decode())
        self.assertEqual(json_response["likes"], 1)
        self.assertEqual(json_response["num_votes"], 1)
        #User 2 voting up
        request = factory.post(vote_url)
        request.user = CustomUser.objects.create(username='testuser2', email="test2@test.com")
        view = OfferVoteView
        response = view.post(self=view, request=request, pk=id, mode="like")
        json_response=json.loads(response.content.decode())
        self.assertEqual(json_response["likes"], 2)
        self.assertEqual(json_response["num_votes"], 2)

    def test_vote_down(self):
        """
        Checks if system counts up votes correctly
        """
        id = self.offer.id
        vote_url = "/offers/vote/{}/like".format(id)
        view = OfferVoteView
        # User 1 voting down
        factory = RequestFactory()
        request = factory.post(vote_url)
        request.user = CustomUser.objects.create(username='testuser', email="test@test.com")
        response = view.post(self=view, request=request, pk=id, mode="dislike")
        json_response = json.loads(response.content.decode())
        self.assertEqual(json_response["likes"], -1)
        self.assertEqual(json_response["num_votes"], 1)
        # User 2 voting down
        request = factory.post(vote_url)
        request.user = CustomUser.objects.create(username='testuser2', email="test2@test.com")
        view = OfferVoteView
        response = view.post(self=view, request=request, pk=id, mode="dislike")
        json_response = json.loads(response.content.decode())
        self.assertEqual(json_response["likes"], -2)
        self.assertEqual(json_response["num_votes"], 2)

    def test_change_vote(self):
        """
        Checks if changing vote works as intended
        """
        id = self.offer.id
        vote_url = "/offers/vote/{}/dislike".format(id)
        view = OfferVoteView
        # User 1 voting down
        factory = RequestFactory()
        request = factory.post(vote_url)
        request.user = CustomUser.objects.create(username='testuser', email="test@test.com")
        response = view.post(self=view, request=request, pk=id, mode="dislike")
        json_response = json.loads(response.content.decode())
        self.assertEqual(json_response["likes"], -1)
        self.assertEqual(json_response["num_votes"], 1)
        response = view.post(self=view, request=request, pk=id, mode="like")
        json_response = json.loads(response.content.decode())
        self.assertEqual(json_response["likes"], 1)
        self.assertEqual(json_response["num_votes"], 1)