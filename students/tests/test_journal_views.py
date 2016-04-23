from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from ..models import MonthJournal, Group


class JuornalViewsTest(TestCase):
    """Test journal views"""

    fixtures = ['students_test_data.json']

    def setUp(self):
        self.url = reverse('journal')
        self.url_pk = reverse('journal', kwargs={'pk':'1'})
        self.client = Client()
        self.client.login(username='admin', password='admin')
        #student, created = Student.objects.get_or_create(
        #    first_name = 'f_name',
        #    last_name = 'l_name')
        #MonthJournal.objects.get_or_create(
        #    student=student,
        #    date = datetime.today())

    def test_post(self):
        post_data = {
            'date': '2000-01-01',
            'present': '1',
            'pk': '1',}
        response = self.client.post(self.url, post_data)

        # do we have OK status from the server?
        self.assertEqual(response.status_code, 200)
        # check content type
        self.assertEqual(response.get('Content-Type'),
                         'application/json')
        # check content
        self.assertEqual(response.content, '{"status": "success"}')

        # check MonthJournal item is created and the day is checked
        journal_item = MonthJournal.objects.get(id=1)
        self.assertTrue(journal_item.present_day1)

    def test_get(self):
        response = self.client.get(self.url)
        # do we have OK status from the server?
        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.context['is_paginated'])
        self.assertTrue(response.context['next_month'])
        self.assertTrue(response.context['prev_month'])
        self.assertTrue(response.context['cur_month'])
        self.assertTrue(response.context['students'])

    def test_get_pk_month(self):
        response = self.client.get(self.url_pk, {'month':'2000-02-01'})

        # do we have OK status from the server?
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['students']), 1)
        self.assertEqual(response.context['cur_month'], '2000-02-01')
        self.assertEqual(response.context['prev_month'], '2000-01-01')
        self.assertEqual(response.context['next_month'], '2000-03-01')

    def test_current_group(self):
        # set group as currently selected group
        group = Group.objects.filter(title='Group2')[0]
        self.client.cookies['current_group'] = group.id

        # make request to the server to get homepage page
        response = self.client.get(self.url)

        # in group1 we have only 1 student
        self.assertEqual(len(response.context['students']), 1)
