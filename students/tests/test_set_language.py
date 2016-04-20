from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse


@override_settings(LANGUAGE_CODE='en')
class SetLanguageTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_set_language(self):
        # try with specified 'lang' and 'return-path'
        response = self.client.post(reverse('set_language'),
                                    {'lang': 'uk',
                                     'return-path': reverse('groups')})
        self.assertEqual(self.client.cookies.get('django_language').value,
                         'uk')
        self.assertEqual(response.url, 'http://testserver/groups/')

        # try without specified 'lang' and 'return-path'
        response = self.client.post(reverse('set_language'),{})
        self.assertEqual(self.client.cookies.get('django_language').value,
                         'en')
        self.assertEqual(response.url, 'http://testserver/')
