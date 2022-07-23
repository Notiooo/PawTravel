import datetime
import tempfile

from django.test import TestCase
from django.urls import reverse
from offers.models import Offer, OfferCategory
from users.models import CustomUser
from comments.models import Comment
from parameterized import parameterized, parameterized_class

from travel_guides.models import Guide, GuideCategory, Country


class CommentsTestCase(TestCase):
    """Base test case with one offer in the base"""

    def setUp(self):
        """Inserts the necessary test objects into the database"""

        mock_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
        user = CustomUser.objects.create(username='user1', password='password', email='user1@gmail.com')
        user.set_password('password')
        user.save()
        OfferCategory.objects.create(name="TestCategory")
        Offer.objects.create(title="TestTitle", short_content="Example short content", content="<b>Styled content</b>",
                             category=OfferCategory.objects.get(id=1), image=mock_file,
                             offer_ends=datetime.datetime(2022, 12, 13, 14, 57, 11, 342380), author=user,
                             original_price=1999.99,
                             offer_price=989.99, link="http://google.com")

        category = GuideCategory(name="Test Category").save()
        country = Country(name="Test Country").save()
        Guide.objects.create(title="TestGuide", author=user, category=category, country=country,
                             image=tempfile.NamedTemporaryFile(suffix=".jpg").name)


@parameterized_class(('page', 'slug_url'), [
    ('offer',                       'testtitle'),
    ('travel_guides:guide_detail',  'testguide'),
 ])
class DetailOfferLoggedInCommentsTestCase(CommentsTestCase):
    """
    The case where the user is logged in and we check if he has the
    capabilities available to the logged in user
    """

    def setUp(self):
        super(DetailOfferLoggedInCommentsTestCase, self).setUp()
        self.client.login(username='user1', password='password')

    def test_textarea_placeholder(self):
        response = self.client.get(reverse(self.page, kwargs={'pk': 1, 'slug_url': self.slug_url}))
        self.assertContains(response, 'Tell us what you think')

    def test_comment_button(self):
        response = self.client.get(reverse(self.page, kwargs={'pk': 1, 'slug_url': self.slug_url}))
        self.assertContains(response, 'Send a comment')


class DetailOfferLoggedOutCommentsTestCase(CommentsTestCase):
    """
    The case where the user is logged in and we check if he has the
    capabilities available to the logged in user
    """

    def setUp(self):
        super(DetailOfferLoggedOutCommentsTestCase, self).setUp()

    @parameterized.expand([
         ('offer',                      'testtitle', '/offers/testtitle-1/'),
         ('travel_guides:guide_detail', 'testguide', '/guides/testguide-1/'),
    ])
    def test_no_logged_in_message(self, page, slug_url, link):
        response = self.client.get(reverse(page, kwargs={'pk': 1, 'slug_url': slug_url}))
        self.assertContains(response, 'You may write your own comment! '
                                      'All you have to do is '
                                      '<a href="/users/login/?next=' + link + '">sign in</a>')


class DetailOfferWithoutCommentsTestCase(CommentsTestCase):
    """A case to check the correct behavior when there are no comments"""

    @parameterized.expand([
         ('offer',                      'testtitle'),
         ('travel_guides:guide_detail', 'testguide'),
    ])
    def test_no_comments(self, page, slug_url):
        response = self.client.get(reverse(page, kwargs={'pk': 1, 'slug_url': slug_url}))
        self.assertContains(response, '0 comments')


@parameterized_class(('page', 'slug_url', 'commented_object'), [
    ('offer',                       'testtitle', Offer),
    ('travel_guides:guide_detail',  'testguide', Guide),
 ])
class DetailOfferWithCommentsTestCase(CommentsTestCase):
    """A case to check the correct behavior when there are comments"""

    def setUp(self):
        """Inserts the necessary test objects into the database"""
        super().setUp()

        self.mock_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.time = datetime.datetime(year=2020, month=5, day=17, hour=16, minute=50)
        self.comment_user = CustomUser.objects.create(username='user2', email='user2@gmail.com')
        self.offer = self.commented_object.objects.get(id=1)
        self.comment = Comment.objects.create(text="Test comment content", author=self.comment_user, object_id=1,
                                              content_object=self.offer)
        self.comment.date = self.time
        self.comment.save()

    def test_one_comment(self):
        response = self.client.get(reverse(self.page, kwargs={'pk': 1, 'slug_url': self.slug_url}))
        self.assertContains(response, '1 comment')

    def test_correct_user(self):
        response = self.client.get(reverse(self.page, kwargs={'pk': 1, 'slug_url': self.slug_url}))
        self.assertContains(response, 'user2')

    def test_correct_comment_text(self):
        response = self.client.get(reverse(self.page, kwargs={'pk': 1, 'slug_url': self.slug_url}))
        self.assertContains(response, 'Test comment content')

    def test_correct_date(self):
        response = self.client.get(reverse(self.page, kwargs={'pk': 1, 'slug_url': self.slug_url}))
        self.assertContains(response, 'May 17, 2020, 4:50 p.m.')
