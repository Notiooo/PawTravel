import datetime

from django import forms
from . import models
from django.core.cache import cache


class ActionTimeout:
    """
    It is used in situations where a certain action of a user should not be allowed to do infinite amount of times
    So it's a kind of time block between every signle action
    """
    @staticmethod
    def _key(action, username):
        return '{}_timeout_{}'.format(action, username)

    @staticmethod
    def _value(time):
        return {
            'last_attempt': time,
        }

    @staticmethod
    def delete(action, username):
        cache.delete(ActionTimeout._key(action, username))

    @staticmethod
    def set(action, username, time):
        key = ActionTimeout._key(action, username)
        value = ActionTimeout._value(time)
        cache.set(key, value)

    @staticmethod
    def get(action, username):
        key = ActionTimeout._key(action, username)
        return cache.get(key)


class CommentForm(forms.ModelForm):
    time_between_comments = 30  # in seconds
    action = 'add_comment'

    def __init__(self, form_object=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_object = form_object

    class Meta:
        model = models.Comment
        fields = ['text']

    def clean(self):
        username = self.cleaned_data.get('username')
        cache_results = ActionTimeout.get(self.action, username)
        now = datetime.datetime.now()
        last_attempt = cache_results['last_attempt'] if cache_results else False
        if last_attempt > (now - datetime.timedelta(seconds=self.time_between_comments)).timestamp():
            raise forms.ValidationError('You are adding your comments too quickly!')
        return super(CommentForm, self).clean()

    def form_valid(self, form, request):
        comment = self.save(commit=False)
        comment.author = request.user
        comment.content_object = self.form_object
        comment.object_id = self.form_object.id
        comment.save()

    def save(self, *args, **kwargs):
        ActionTimeout.set(self.action, self.cleaned_data.get('username'), datetime.datetime.now().timestamp())
        return super(CommentForm, self).save(*args, **kwargs)