from datetime import datetime

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from students.models import Student, Group


class TestStudentList(TestCase):

    def setUp(self):
        # create groups
        group1, created = Group.objects.get_or_create(
            title='MtM-1')
        group2, created = Group.objects.get_or_create(
            title='MtM-2')
        Student.objects.get_or_create(
            first_name="f_name1",
            last_name="l_name1",
            birthday = datetime.today(),
            ticket='1',
            student_group=group1)
        Student.objects.get_or_create(
            first_name="f_name2",
            last_name="l_name2",
            birthday = datetime.today(),
            ticket='2',
            student_group=group2)
        Student.objects.get_or_create(
            first_name="f_name3",
            last_name="l_name3",
            birthday = datetime.today(),
            ticket='3',
            student_group=group2)
        Student.objects.get_or_create(
            first_name="f_name4",
            last_name="l_name4",
            birthday = datetime.today(),
            ticket='4',
            student_group=group2)

        # remember test browser
        self.client = Client()

        self.url = reverse('home')

    def test_students_list(self):
        # make request to the server to get homepage page
        response = self.client.get(self.url)

        # do we have OK status from the server?
        self.assertEqual(response.status_code, 200)

        # do we have student name on a page?
        self.assertIn('f_name1', response.content)

        # do we have link to student edit form?
        self.assertIn(reverse('students_edit',
            kwargs={'pk': Student.objects.all()[0].id}),
            response.content)

        # ensure we got 3 students, pagination limit is 3
        self.assertEqual(len(response.context['students']), 3)


