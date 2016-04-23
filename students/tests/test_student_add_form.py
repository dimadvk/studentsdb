import os

from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import transaction

from ..models import Student

@override_settings(LANGUAGE_CODE='en')
class TestStudentAddForm(TestCase):
    """Test form for adding new student"""

    fixtures = ['students_test_data.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('students_add')
        # prepare files for testing Photo field
        file_too_big = open('file_too_big.tmp', 'w+')
        file_too_big.write('x'*(2*1024*1024+1))
        file_too_big.close()
        file_not_image = open('file_not_image.tmp', 'w+')
        #file_not_image.write('x'*(2*1024*1024-1))
        file_not_image.close()

    def test_get_form(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url)

        # check response status code
        self.assertEqual(response.status_code, 200)

        # check page title, few field titles and button on edit form
        self.assertIn('Add Student', response.content)
        self.assertIn('Ticket', response.content)
        self.assertIn('Last name', response.content)
        self.assertIn('name="add_button"', response.content)
        self.assertIn('action="%s"' % self.url, response.content)
        self.assertIn('Photo', response.content)

    def test_post_wrong_data(self):
        self.client.login(username='admin', password='admin')
        ### post empty form
        response = self.client.post(self.url,
                                    {'first_name': '',
                                     'last_name': '',
                                     'birthday': '',
                                     'ticket': '',
                                     'student_group': '',
                                     'add_button':'Save'},
                                    follow=True)
        # check for errors
        self.assertIn('First Name field is required', response.content)
        self.assertIn('Last Name field is required', response.content)
        self.assertIn('Birthday date is required', response.content)
        self.assertIn('Ticket number is required', response.content)
        self.assertIn('Select group for student', response.content)

        ### post wrong format of birthday date and wrong group_id
        response = self.client.post(self.url,
                                    {'first_name': 'xxx',
                                     'last_name': 'xxx',
                                     'birthday': 'xxx',
                                     'ticket': '123',
                                     'student_group': '999',
                                     'add_button': 'Save'},
                                    follow=True)
        # check for errors
        self.assertIn('Please, enter the correct date (Ex. 1984-12-30)', response.content)
        self.assertIn('Select group for student', response.content)

        ### post wrong image file

        # post too big file (size more than 2MB)
        with open('file_too_big.tmp', 'rb') as photo:
            response = self.client.post(self.url,
                                        {'first_name': 'xxx',
                                         'last_name': 'xxx',
                                         'birthday': '1984-12-30',
                                         'ticket': '123',
                                         'photo': photo,
                                         'student_group': '1',
                                         'add_button': 'Save'},
                                        follow=True)
        # check for errors
        self.assertIn('The file is too big. Must be less then 2MB', response.content)
        # post file normal size but not an image
        with open('file_not_image.tmp', 'rb') as photo:
            response = self.client.post(self.url,
                                        {'first_name': 'xxx',
                                         'last_name': 'xxx',
                                         'birthday': '1984-12-30',
                                         'ticket': '123',
                                         'photo': photo,
                                         'student_group': '1',
                                         'add_button': 'Save'},
                                        follow=True)
        # check for errors
        self.assertIn('File is not an image', response.content)

    def test_post_right_data(self):
        photo_path = os.path.join(settings.BASE_DIR, 'students/fixtures/test.jpg')
        self.client.login(username='admin', password='admin')
        with open(photo_path, 'rb') as photo:
            response = self.client.post(self.url,
                                        {'first_name': 'new_fname',
                                         'last_name': 'new_lname',
                                         'middle_name': '',
                                         'birthday': '1984-12-30',
                                         'ticket': '123',
                                         'photo': photo,
                                         'student_group': '1',
                                         'notes': '',
                                         'add_button':'Save'},
                                        follow=True)
        # check response status
        self.assertEqual(response.status_code, 200)
        # check new student
#        with transaction.atomic():
#            student = Student.objects.filter(
#                first_name='new_fname', last_name='new_lname')
#            self.assertEqual(len(student), 1)
#        # check saved photo
#        self.assertTrue(os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'test.jpg')))
        # check the right redirection
        self.assertIn('Student &quot;new_fname new_lname&quot; sucessfully added!',
                         response.content)
        self.assertEqual(response.redirect_chain[0][0],
                         'http://testserver/')

    def test_access(self):
        response = self.client.get(self.url, follow=True)
        # response status must be 200, and content - login form
        self.assertEqual(response.status_code, 200)
        self.assertIn('Log in', response.content)

    def tearDown(self):
        if os.path.isfile('file_too_big.tmp'):
            os.remove('file_too_big.tmp')
        if os.path.isfile('file_not_image.tmp'):
            os.remove('file_not_image.tmp')
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'test.jpg')):
            os.remove(os.path.join(settings.MEDIA_ROOT, 'test.jpg'))

