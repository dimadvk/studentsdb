from django.test import TestCase, Client, override_settings

from ..models import Group


class TestGroupsList(TestCase):

    fixtures = ['students_test_data.json']

    def setUp(self):
        self.client = Client()

    def test_access(self):
        pass
