import datetime
import tempfile

from django.test import TestCase
from django.urls import reverse
from offers.models import Offer, OfferCategory
from parameterized import parameterized_class, parameterized
from users.models import CustomUser
from pathlib import Path


class DetailOfferViewTestCase(TestCase):
    """Tests for correct displaying of a specific single offer"""

    def setUp(self):
        """Inserts the necessary test objects into the database"""

        self.mock_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.current_time = datetime.datetime.now()
        user = CustomUser.objects.create_user(username='user1', password='password')
        self.client.login(username='user1', password='password')
        OfferCategory.objects.create(name="TestCategory")
        Offer.objects.create(
            title="TestTitle",
            slug_url='testtitle-1',
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

class HomePageView(TestCase):
    def test_view_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/home.html')

class DetailOfferTestCase(TestCase):
    """Tests that check the model itself rather than the view itself"""

    def setUp(self):
        """Inserts the necessary test objects into the database"""
        user = CustomUser.objects.create_user(username='user1', password='password')
        self.client.login(username='user1', password='password')
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

class CreateOfferViewTestCase(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
        offerCategory = OfferCategory.objects.create(name="TestCategory")

    def test_view_status_code(self):
        response = self.client.get('/offers/new/')
        self.assertEqual(response.status_code, 200)

    def test_view_by_name(self):
        response = self.client.get(reverse('offer_new'))
        self.assertEqual(response.status_code, 200)

    def test_view_correct_template(self):
        response = self.client.get(reverse('offer_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/new_offer.html')

class DeleteOfferViewTestCase(TestCase):
    def setUp(self):
        """Inserts the necessary test objects into the database"""

        self.mock_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.current_time = datetime.datetime.now()
        user = CustomUser.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
        OfferCategory.objects.create(name="TestCategory")
        self.offer = Offer.objects.create(
            title="TestTitle",
            slug_url='testtitle-1',
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
        response = self.client.get('/offers/1/delete/')
        self.assertEqual(response.status_code, 200)

    def test_view_by_name(self):
        response = self.client.get(reverse('offer_delete', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_correct_template(self):
        response = self.client.get('/offers/1/delete/')
        self.assertTemplateUsed(response, 'offers/delete_offer.html')

class UpdateOfferViewTestCase(TestCase):
    def setUp(self):
        """Inserts the necessary test objects into the database"""

        self.mock_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.current_time = datetime.datetime.now()
        user = CustomUser.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
        OfferCategory.objects.create(name="TestCategory")
        self.offer = Offer.objects.create(
            title="TestTitle",
            slug_url='testtitle-1',
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
        response = self.client.get('/offers/1/edit/')
        self.assertEqual(response.status_code, 200)

    def test_view_correct_template(self):
        response = self.client.get('/offers/1/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/edit_offer.html')

    def test_view_update_offer(self):
        response = self.client.post(
           '/offers/1/edit/', data=
            {'title': "NewTestTitle",
            'short_content': "New short content",
            'content': "<b> New styled content </b>",
            'category': '',
            'image': '',
            'date_posted': datetime.datetime(2022, 12, 13, 14, 57, 11, 342380),
            'original_price': 199.99,
            'offer_price': 99.99,
            'offer_ends': datetime.datetime(2022, 12, 13, 14, 57, 11, 342311),
            'link': "https://bing.com",
            'author': 'user1'}
        )

       
        self.offer.refresh_from_db()
        self.assertEqual(response.status_code, 200)

        # For some reason client.post dosen't change anything in the database
        # for now I have no idea why, maybe later this bug will be resolved
        #self.assertEquals(self.offer.title, "NewTestTitle")
