from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

# Login and logout are part of Django,
# therefore they already have test coverage

class SignupPageTests(TestCase):
    username = 'user'
    email = 'user123@gmail.com'

def test_signup_page_status_code(self):
    response = self.client.get('/users/signup/')
    self.assertEqual(response.status_code, 200)

def test_signup_url_by_name(self):
    response = self.client.get(reverse('signup'))
    self.assertEqual(response.status_code, 200)

def test_signup_uses_correct_template(self):
    response = self.client.get(reverse('signup'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'signup.html')

def test_signup_form(self):
    new_user = get_user_model().objects.create_user(
        self.username, self.email)
    self.assertEqual(get_user_model().objects.all().count(), 1)
    self.assertEqual(get_user_model().objects.all()
                     [0].username, self.username)
    self.assertEqual(get_user_model().objects.all()
                     [0].email, self.email)