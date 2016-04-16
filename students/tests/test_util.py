from datetime import datetime

from django.test import TestCase
from django.http import HttpRequest

from students.models import Student, Group
from students.util import get_current_group, get_groups, paginate


class UtilsTestCase(TestCase):
    """Test functions from util module"""

    def setUp(self):
        # create set of users and groups in database
        group1, created = Group.objects.get_or_create(
            id=1,
            title="Group1"
        )
        student1, created = Student.objects.get_or_create(
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
            student_group=group1)
        Student.objects.get_or_create(
            first_name="f_name3",
            last_name="l_name3",
            birthday = datetime.today(),
            ticket='3',
            student_group=group1)
        Student.objects.get_or_create(
            first_name="f_name4",
            last_name="l_name4",
            birthday = datetime.today(),
            ticket='4',
            student_group=group1)

        group1.leader = student1
        group1.save()


    def test_get_current_group(self):
        # preapre requesto object to pass to utility function
        request = HttpRequest()

        # test with no group in cookie
        request.COOKIES['current_group'] = ''
        self.assertEqual(None, get_current_group(request))

        # test with invalid group id
        request.COOKIES['current_group'] = '123333'
        self.assertEqual(None, get_current_group(request))

        # test with proper group id
        group = Group.objects.filter(title='Group1')[0]
        request.COOKIES['current_group'] = str(group.id)
        self.assertEqual(group, get_current_group(request))

    def test_get_groups(self):

        request = HttpRequest()
        groups_from_db = Group.objects.all()
        groups_from_func = get_groups(request)

        # check the count of groups in returned list
        self.assertEqual(len(groups_from_func), len(groups_from_db))

        # check if data in returned list is a data of groups
        self.assertEqual(groups_from_func[0],
                         {'id': 1,
                          'title': u'Group1',
                          'leader': u'f_name1 l_name1',
                          'selected': False}
                        )

    def test_paginate(self):
        request = HttpRequest()

        objects = Student.objects.all()

        # try without page in request
        context = paginate(objects, 3, request, {}, var_name='students')
        self.assertTrue(isinstance(context, dict))
        self.assertEqual(len(context.get('students')), 3)
        self.assertEqual(context.get('is_paginated'), True)
        self.assertTrue(context.has_key('page_obj'))
        self.assertTrue(context.has_key('paginator'))

        # try with page=2 in request
        request.GET.update({'page':'2'})
        context = paginate(objects, 3, request, {}, var_name='students')
        self.assertTrue(isinstance(context, dict))
        self.assertEqual(len(context.get('students')), 1)
        self.assertEqual(context.get('is_paginated'), True)
        self.assertTrue(context.has_key('page_obj'))
        self.assertTrue(context.has_key('paginator'))


