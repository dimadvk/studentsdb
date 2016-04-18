import os

from django.test import TestCase
from django.core.management import call_command
from django.utils.six import StringIO

class CommandsTest(TestCase):

    fixtures = ['students_test_data.json',]

    def test_stcount(self):

        out = StringIO()
        # test for student, group and user models
        call_command('stcount',
                     'student', 'group', 'user',
                     stdout=out)
        self.assertEqual(out.buflist,
                         ['Number of students in database: 4\n',
                          'Number of groups in database: 2\n',
                          'Number of users in database: 1\n']
                        )
