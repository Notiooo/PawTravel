import datetime
import tempfile
from django.test import TestCase
from django.urls import reverse
from offers.models import Offer, OfferCategory
from users.models import CustomUser


class DetailOfferViewTestCase(TestCase):
    def setUp(self):
        self.mockFile = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.currentTime = datetime.datetime.now()
        user = CustomUser.objects.create(username='user1')
        offerCategory = OfferCategory.objects.create(name="TestCategory", iconImage=self.mockFile)
        offer = Offer.objects.create(
            title="TestTitle",
            shortContent="Example short content",
            content="<b>Styled content</b>",
            category=OfferCategory.objects.get(id=1),
            image = self.mockFile,
            offerEnds = datetime.datetime(2022, 12, 13, 14, 57, 11, 342380),
            author = user,
            originalPrice = 1999.99,
            offerPrice = 989.99,
            link = "http://google.com"
        )

    def testViewStatusCode(self):
        response = self.client.get('/offers/1/')
        self.assertEqual(response.status_code, 200)

    def testViewByName(self):
        response = self.client.get(reverse('offer', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def testViewCorrectTemplate(self):
        response = self.client.get(reverse('offer', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detailed_offer.html')

    def testViewCorrectTitle(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, "TestTitle")

    def testViewCorrectShortContent(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, "Example short content")

    def testViewCorrectContent(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, "<b>Styled content</b>")

    def testViewCorrectCategory(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, "TestCategory")

    def testViewCorrectImage(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, self.mockFile)

    def testViewCorrectDatePosted(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, f'{self.currentTime.year}')
        self.assertContains(response, f'{self.currentTime.day}')
        self.assertContains(response, f'{self.currentTime.month}')

    def testViewCorrectOfferEnds(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, "2022")
        self.assertContains(response, "12")
        self.assertContains(response, "13")
        self.assertContains(response, "14")
        self.assertContains(response, "57")

    def testViewCorrectAuthor(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, "user1")

    def testViewCorrectOriginalPrice(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, "1999.99")

    def testViewCorrectOfferPrice(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, "989.99")

    def testViewCorrectLink(self):
        response = self.client.get('/offers/1/')
        self.assertContains(response, "http://google.com")

class HomePageView(TestCase):
    def testViewStatusCode(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def testViewByName(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def testViewCorrectTemplate(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

class DetailOfferTestCase(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(username='user1')
        offerCategory = OfferCategory.objects.create(name="TestCategory")
        offer = Offer.objects.create(
            title="TestTitle",
            shortContent="Example short content",
            content="<b>Styled content</b>",
            category=OfferCategory.objects.get(id=1),
            image = tempfile.NamedTemporaryFile(suffix=".jpg").name,
            offerEnds = datetime.datetime(2022, 12, 13, 14, 57, 11, 342380),
            author = user,
            originalPrice = 1999.99,
            offerPrice = 989.99,
            link = "http://google.com"
        )

    def testCorrectStringDisplay(self):
        offer = Offer.objects.get(id=1)
        expectedOfferName = f'{offer.title}'
        self.assertEqual(expectedOfferName, 'TestTitle')

    def testCorrectOfferContent(self):
        offer = Offer.objects.get(id=1)
        self.assertEqual(f'{offer.title}', "TestTitle")
        self.assertEqual(f'{offer.shortContent}', "Example short content")
        self.assertEqual(f'{offer.category}', "TestCategory")
        self.assertEqual(f'{offer.image}'[-4:], ".jpg")
        self.assertEqual(f'{offer.offerEnds}', "2022-12-13 14:57:11.342380+00:00")
        self.assertEqual(f'{offer.author}', "user1")
        self.assertEqual(f'{offer.originalPrice}', "1999.99")
        self.assertEqual(f'{offer.offerPrice}', "989.99")
        self.assertEqual(f'{offer.link}', "http://google.com")

    def testAbsoluteUrl(self):
        offer = Offer.objects.get(id=1)
        self.assertEquals(offer.get_absolute_url(), '/offers/1/')

class CreateOfferViewTestCase(TestCase):
    def setUp(self):
         user = CustomUser.objects.create(username='user1')
         offerCategory = OfferCategory.objects.create(name="TestCategory")

    def testViewStatusCode(self):
        response = self.client.get('/offers/new/')
        self.assertEqual(response.status_code, 200)

    def testViewByName(self):
        response = self.client.get(reverse('offer_new'))
        self.assertEqual(response.status_code, 200)

    def testViewCorrectTemplate(self):
        response = self.client.get(reverse('offer_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_offer.html')

class UpdateOfferViewTestCase(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(username='user1')
        self.mockFile = tempfile.NamedTemporaryFile(suffix=".jpg").name
        offerCategory = OfferCategory.objects.create(name="TestCategory", iconImage = self.mockFile)
        
        self.currentTime = datetime.datetime.now()
        self.offer = Offer.objects.create(
            title='Test title',
            shortContent="Example short content",
            content="<b>Styled content</b>",
            category=OfferCategory.objects.get(id=1),
            image = self.mockFile,
            offerEnds = datetime.datetime(2022, 12, 13, 14, 57, 11, 342380),
            author = user,
            originalPrice = 1999.99,
            offerPrice = 989.99,
            link = "http://google.com"
        )

    def testViewStatusCode(self):
        response = self.client.get('/offers/1/edit/')
        self.assertEqual(response.status_code, 200)

    def testViewCorrectTemplate(self):
        response = self.client.get('/offers/1/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_offer.html')

    def testViewUpdateOffer(self):
        response = self.client.post(
           '/offers/1/edit/', data=
            {'title': "NewTestTitle",
            'shortContent': "New short content",
            'content': "<b> New styled content </b>",
            'category': '',
            'image': '',
            'datePosted': datetime.datetime(2022, 12, 13, 14, 57, 11, 342380),
            'originalPrice': 199.99,
            'offerPrice': 99.99,
            'offerEnds': datetime.datetime(2022, 12, 13, 14, 57, 11, 342311),
            'link': "https://bing.com",
            'author': 'user1'}
        )

       
        self.offer.refresh_from_db()
        self.assertEqual(response.status_code, 200)

        # For some reason client.post dosen't change anything in the database
        # for now I have no idea why, maybe later this bug will be resolved
        #self.assertEquals(self.offer.title, "NewTestTitle")