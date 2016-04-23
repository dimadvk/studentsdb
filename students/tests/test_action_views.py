from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from ..models import Action


class ActionViewsTest(TestCase):
    """Test view for "action journal" page"""

    fixtures = ['students_test_data.json']

    def setUp(self):
        self.client = Client()
        Action.objects.get_or_create(
            action_detail='action detail 1',
            model_name='model_1',
            model_verbose_name='model verbose name 1')

    def test_pagination(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('action_journal'))
        self.assertTrue(response.context_data.has_key('is_paginated'))
        self.assertTrue(response.context_data.has_key('actions'))
