"""Test fill_db management command"""
from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth.models import User

from ..models import Student, Group


class CommandFillDbTest(TestCase):
    """Test class for fill_db management command """

    def test_right_options(self):
        """Passing right options to command"""
        # test for student, group and user models
        call_command('fill_db',
                     student=3, group=2, user=1)

        self.assertEqual(len(Student.objects.all()), 3)
        self.assertEqual(len(Group.objects.all()), 2)
        self.assertEqual(len(User.objects.all()), 1)

    def test_wrong_options(self):
        # test student option with wrong parameters
        with self.assertRaises(ValueError):
            call_command('fill_db', student='100')
        with self.assertRaises(ValueError):
            call_command('fill_db', student='0')
        with self.assertRaises(ValueError):
            call_command('fill_db', student='x')

        # test group option with wrong parameters
        with self.assertRaises(ValueError):
            call_command('fill_db', group='100')
        with self.assertRaises(ValueError):
            call_command('fill_db', group='0')
        with self.assertRaises(ValueError):
            call_command('fill_db', group='x')

        # test user option with wrong parameters
        with self.assertRaises(ValueError):
            call_command('fill_db', user='100')
        with self.assertRaises(ValueError):
            call_command('fill_db', user='0')
        with self.assertRaises(ValueError):
            call_command('fill_db', user='x')


