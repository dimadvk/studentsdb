from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse

from ..models import Group

@override_settings(LANGUAGE_CODE='en')
class TestGroupsList(TestCase):

    fixtures = ['students_test_data.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('groups')

    def test_access(self):
        response = self.client.get(self.url, follow=True)

        # we must have response status 200 and login page
        self.assertEqual(response.status_code, 200)
        self.assertIn('Log in', response.content)
        # check the redirection link
        self.assertEqual(response.redirect_chain[0][0],
             'http://testserver/users/login/?next=/groups/')

    def test_groups_list(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url)

        # response status code must be 200
        self.assertEqual(response.status_code, 200)
        # title 'Groups' and button 'Create Group' must be on page
        self.assertIn('Groups', response.content)
        self.assertIn('Create Group', response.content)
        # check pagination attribute
        self.assertTrue(response.context['is_paginated'])
        # check if we have exactly 3 groups on page
        self.assertEqual(len(response.context['groups']), 3)

    def test_pagination(self):
        # test page=2
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url, {'page': '2'})
        # check response status code
        self.assertEqual(response.status_code, 200)
        # do we have only one object, Group4?
        self.assertEqual(len(response.context['groups']), 1)
        self.assertIn('Group4', response.content)

    def test_current_group(self):
        pass

    def test_order_by(self):
        pass

    def test_reverse_order(self):
        pass

class TestGroupAdd(TestCase):
    pass

class TestGroupUpdate(TestCase):
    pass

class TestGroupDelete(TestCase):
    pass
