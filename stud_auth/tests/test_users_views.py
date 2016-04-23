from django.test import TestCase, override_settings, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


@override_settings(LANGUAGE_CODE='en')
class TestUsersList(TestCase):

    fixtures = ['stud_auth_test_data.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('users_list')

    def test_access(self):
        response = self.client.get(self.url, follow=True)
        # status code 200
        self.assertEqual(response.status_code, 200)
        # login page
        self.assertIn('Log in', response.content)
        # right link
        self.assertEqual(response.redirect_chain[0][0],
             'http://testserver/users/login/?next=/users/profiles/')

    def test_users_list(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url)
        # users list page
        self.assertIn('Users List', response.content)
        # count of users in context
        users_count = User.objects.all().count()
        self.assertEqual(len(response.context['users']), users_count)


@override_settings(LANGUAGE_CODE='en')
class TestProfile(TestCase):

    fixtures = ['stud_auth_test_data.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('profile')

    def test_access(self):
        response = self.client.get(self.url, follow=True)
        # status code 200
        self.assertEqual(response.status_code, 200)
        # login page
        self.assertIn('Log in', response.content)
        # right link
        self.assertEqual(response.redirect_chain[0][0],
             'http://testserver/users/login/?next=/users/profile/')

    def test_profile(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url)
        # page contains links to "change password" and "edit profile"
        self.assertIn('/users/password_change/',
                      response.content)
        self.assertIn('/users/profile/edit/',
                      response.content)
        # response context contains object of user 'admin'
        user = User.objects.get(id=1)
        self.assertEqual(user, response.context['user'])


@override_settings(LANGUAGE_CODE='en')
class TestProfileEdit(TestCase):

    fixtures = ['stud_auth_test_data.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('user_profile_edit')

    def test_access(self):
        response = self.client.get(self.url, follow=True)
        # status code 200
        self.assertEqual(response.status_code, 200)
        # login page
        self.assertIn('Log in', response.content)
        # right link
        self.assertEqual(response.redirect_chain[0][0],
             'http://testserver/users/login/?next=/users/profile/edit/')

    def test_get_form(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url)
        # form fields, 'Save' button
        self.assertIn('name="photo"', response.content)
        self.assertIn('name="mobile_phone"', response.content)
        self.assertIn('name="passport_id"', response.content)
        self.assertIn('name="address"', response.content)
        self.assertIn('name="add_button"', response.content)
        ## title: 'username - edit' or 'full_name - edit'
        # try user without full name
        self.assertIn('admin - edit', response.content)
        # try user with full name
        self.client.logout()
        self.client.login(username='user2', password='user2')
        response = self.client.get(self.url)
        self.assertIn('User2 Last Name - edit', response.content)
#        self.client.logout()

    def test_post_data(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(self.url,
                                    {'photo': '',
                                     'mobile_phone': '0001234567',
                                     'passport_id': '123456',
                                     'address': 'user address'},
                                   follow=True)
        # check response status code
        self.assertEqual(response.status_code, 200)
        # right redirection
        self.assertEqual(response.redirect_chain[0][0],
                         'http://testserver/users/profile/')
        # status message about saving
        self.assertIn('Profile successfully updated!', response.content)
        # new user data on a profile page
        self.assertIn('0001234567', response.content)
        self.assertIn('123456', response.content)
        self.assertIn('user address', response.content)


@override_settings(LANGUAGE_CODE='en')
class TestRegistrationForm(TestCase):

    fixtures = ['stud_auth_test_data.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('registration_register')

    def test_get_form(self):
        response = self.client.get(self.url)

        ## title: 'Register Form'
        self.assertIn('Register Form', response.content)
        # form fields, 'Save' button
        self.assertIn('name="username"', response.content)
        self.assertIn('name="email"', response.content)
        self.assertIn('name="password1"', response.content)
        self.assertIn('name="password2"', response.content)
        self.assertIn('name="add_button"', response.content)

    def test_post_data(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(self.url,
                                    {'username': 'TestUser',
                                     'email': 'test@test.com',
                                     'password1': 'test',
                                     'password2': 'test'},
                                   follow=True)
        # check response status code
        self.assertEqual(response.status_code, 200)
        # right redirection
        self.assertEqual(response.redirect_chain[1][0],
                         'http://testserver/')
        # new user in db
        self.assertEqual(User.objects.filter(
            username='TestUser',
            email='test@test.com').count(), 1)
