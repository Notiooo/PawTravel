import datetime
import tempfile

from django.test import TestCase
from django.urls import reverse
from offers.models import Offer, OfferCategory
from users.models import CustomUser
from pathlib import Path


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

    def test_view_status_code(self):
        response = self.client.get('/offers/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_by_name(self):
        response = self.client.get(reverse('offer', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_correct_template(self):
        response = self.client.get(reverse('offer', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/detailed_offer.html')

    def test_view_correct_title(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, "TestTitle")

    def test_view_correct_short_content(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, "Example short content")

    def test_view_correct_content(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, "<b>Styled content</b>")

    def test_view_correct_category(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, "TestCategory")

    def test_view_correct_image(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, Path(self.mock_file).name)

    def test_view_correct_date_posted(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, f'{self.current_time.year}')
        self.assertContains(response, f'{self.current_time.day}')
        self.assertContains(response, f'{self.current_time.month}')

    def test_view_correct_offer_ends(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, "2022")
        self.assertContains(response, "12")
        self.assertContains(response, "13")
        self.assertContains(response, "14")
        self.assertContains(response, "57")

    def test_view_correct_author(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, "user1")

    def test_view_correct_original_price(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, "1999.99")

    def test_view_correct_offer_price(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, "989.99")

    def test_view_correct_link(self):
        response = self.client.get('/offers/1/')
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
        self.assertEquals(offer.get_absolute_url(), '/offers/1/')
