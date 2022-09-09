import json
import time

from django.test import TestCase
from django.utils.timezone import make_aware
from users.models import CustomUser
# Create your tests here.
from django.test.client import RequestFactory, Client
from chat.views import ConversationView, ChatAPIView
from chat.models import Message
from datetime import timedelta, datetime
from unittest import mock

class ConversationListTests(TestCase):
    def setUp(self):
        """
        Preparing three user accounts
        """
        self.user_one = CustomUser(username="TestUser", email="test_email@test.com")
        self.user_one.save()
        self.user_two = CustomUser(username="TestUser2", email="test_email2@test.com")
        self.user_two.save()
        self.user_three = CustomUser(username="TestUser3", email="test_email3@test.com")
        self.user_three.save()


    def test_no_conversation(self):
        """
        Checking if empty array is returned if user has no conversations
        """
        factory = RequestFactory()
        request = factory.get("/messages/inbox/")
        request.user=self.user_one
        view = ConversationView
        response = view.get(self=view, request=request)
        json_response = json.loads(response.content.decode())
        self.assertEqual(json_response, [], "Expected empty array, got {}".format(json_response))

    def test_single_conversation(self):
        """
        Checking is single value is returned if there is only one conversation
        """
        creation_date = datetime.now()
        creation_date = make_aware(creation_date)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value=creation_date
            message = Message(content="Lorem Ipsum", sent_by=self.user_one, sent_to=self.user_two)
            message.save()
        factory = RequestFactory()
        request = factory.get("/messages/inbox/")
        request.user=self.user_one
        view = ConversationView
        response = view.get(self=view, request=request)
        json_response = json.loads(response.content.decode())
        self.assertEqual(json_response, [[2, [message.content, str(message.date)]]], "Expected [2], got {}".format(json_response))

    def test_single_conversation_multiple_messages(self):
        """
        Checking is single value is returned if there is only one conversation
        However this conversation has more than one message
        Checking if there are no dupes
        """
        creation_date = datetime.now()
        creation_date = make_aware(creation_date)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value=creation_date
            Message(content="Lorem Ipsum1", sent_by=self.user_one, sent_to=self.user_two).save()
            Message(content="Lorem Ipsum2", sent_by=self.user_one, sent_to=self.user_two).save()
            last_message=Message(content="Lorem Ipsum3", sent_to=self.user_one, sent_by=self.user_two)
            last_message.save()
        factory = RequestFactory()
        request = factory.get("/messages/inbox/")
        request.user = self.user_one
        view = ConversationView
        response = view.get(self=view, request=request)
        json_response = json.loads(response.content.decode())
        self.assertEqual(json_response, [[2, [last_message.content, str(last_message.date)]]])

    def test_multiple_conversations(self):
        """
        Checking if two values are returned if one user has two conversations
        In 1st conversation he is a receipment
        In 2nd conversation he is the one who sent a message
        """
        message = Message(content="Lorem Ipsum", sent_to=self.user_one, sent_by=self.user_three)
        message_two = Message(content="Lorem Ipsum", sent_by=self.user_one, sent_to=self.user_two)
        message.save()
        message_two.save()
        Message(content="Lorem Ipsum", sent_by=self.user_three, sent_to=self.user_two)
        factory = RequestFactory()
        request = factory.get("/messages/inbox/")
        request.user=self.user_one
        view = ConversationView
        response = view.get(self=view, request=request)
        json_response = json.loads(response.content.decode())
        json_response.sort()
        self.assertEqual(json_response, [[2, [message.content, str(message.date)]], [3, [message_two.content, str(message_two.date)]]])

class ChattingAPITests(TestCase):
    """
    Class responsible for testing if single chat works as intended
    """
    def setUp(self):
        """
        Preparing three user accounts
        """
        self.user_one = CustomUser(username="TestUser", email="test_email@test.com")
        self.user_one.save()
        self.user_two = CustomUser(username="TestUser2", email="test_email2@test.com")
        self.user_two.save()

    def test_sending_messages(self):
        factory = RequestFactory()
        request = factory.get("/conversation")
        request.user = self.user_one
        view = ChatAPIView
        response = view.post(self=view, request=request, receiver=self.user_two.id, content="Lorem Ipsum")
        json_response = json.loads(response.content.decode())
        self.assertEqual(len(json_response), 1, "Expected single message, got {}".format(len(json_response)))
        self.assertEqual(json_response[0]['sent_by_id'], 1)
        self.assertEqual(json_response[0]['sent_to_id'], 2)
        self.assertEqual(json_response[0]['content'], "Lorem Ipsum")

    def test_sending_to_yourself(self):
        """
        Checks if user can send message to himself
        If He tries, he should get 400 code
        """
        factory = RequestFactory()
        request = factory.post("/conversation")
        request.user = self.user_one
        view = ChatAPIView
        response = view.post(self=view, request=request, receiver=self.user_one.id, content="Lorem Ipsum")
        self.assertEqual(response.status_code , 400)

    def test_conversation_fetch(self):
        """
        Checks if user can fetch entire conversation
        Additionally checks if fetch returns same values for both sides of conversation
        """
        creation_date = datetime.now() - timedelta(days=5)
        creation_date = make_aware(creation_date)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value=creation_date
            Message(content="Lorem Ipsum 1", sent_by=self.user_one, sent_to=self.user_two).save()

        creation_date = datetime.now() - timedelta(days=4)
        creation_date = make_aware(creation_date)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value=creation_date
            Message(content="Lorem Ipsum 2", sent_by=self.user_two, sent_to=self.user_one).save()

        creation_date = datetime.now() - timedelta(days=3)
        creation_date = make_aware(creation_date)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value=creation_date
            Message(content="Lorem Ipsum 3", sent_by=self.user_one, sent_to=self.user_two).save()

        creation_date = datetime.now() - timedelta(days=2)
        creation_date = make_aware(creation_date)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value=creation_date
            Message(content="Lorem Ipsum 4", sent_by=self.user_two, sent_to=self.user_one).save()

        creation_date = datetime.now() - timedelta(days=1)
        creation_date = make_aware(creation_date)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value=creation_date
            Message(content="Lorem Ipsum 5", sent_by=self.user_one, sent_to=self.user_two).save()

        factory = RequestFactory()
        request = factory.get("/conversation")
        request.user = self.user_one
        view = ChatAPIView
        response = view.get(self=view, request=request, receiver=self.user_two.id)
        json_response = json.loads(response.content.decode())
        factory = RequestFactory()
        request = factory.get("/conversation")
        request.user = self.user_two
        view = ChatAPIView
        response = view.get(self=view, request=request, receiver=self.user_one.id)
        json_response_two = json.loads(response.content.decode())
        self.assertEqual(len(json_response), 5)
        self.assertEqual(json_response, json_response_two)

    def test_message_filter_range(self):
        """
        This test checks if optional time related parameter works as intended
        """
        Message(content="Lorem Ipsum", sent_by=self.user_one, sent_to=self.user_two).save()
        Message(content="Lorem Ipsum", sent_by=self.user_one, sent_to=self.user_two).save()
        third_message=Message(content="Lorem Ipsum", sent_to=self.user_one, sent_by=self.user_two)
        third_message.save()
        Message(content="Lorem Ipsum", sent_by=self.user_one, sent_to=self.user_two).save()
        Message(content="Lorem Ipsum", sent_by=self.user_one, sent_to=self.user_two).save()
        last_message=Message(content="Lorem Ipsum", sent_to=self.user_one, sent_by=self.user_two)
        last_message.save()
        #Just checking if prepared test data is ok, before real testing
        self.assertEqual(third_message.id, 3, "Third message id error")
        self.assertEqual(last_message.id, 6, "Sixth (last) message id error")
        ###

        factory = RequestFactory()
        request = factory.get("/conversation")
        request.user = self.user_one
        view = ChatAPIView
        response = view.get(self=view, request=request, receiver=self.user_two.id, timestamp=third_message.id)
        json_response = json.loads(response.content.decode())
        self.assertEqual(len(json_response), 3, "Expected 3 messages, got {}".format(len(json_response)))

        factory = RequestFactory()
        request = factory.get("/conversation")
        request.user = self.user_one
        view = ChatAPIView
        response = view.get(self=view, request=request, receiver=self.user_two.id, timestamp=last_message.id)
        json_response = json.loads(response.content.decode())
        self.assertEqual(len(json_response), 0, "Expected 0 messages, got {}".format(len(json_response)))