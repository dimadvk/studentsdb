from datetime import datetime

from django.test import TestCase, override_settings

from ..models import Student, Group, MonthJournal, Action


@override_settings(LANGUAGE_CODE='en')
class ModelsTest(TestCase):
    """Test student model"""

    def setUp(self):
        self.student = Student(first_name='Demo', last_name='Student')
        self.group = Group(title='Title')
        self.group1 = Group(title='Title', leader=self.student)
        self.journal = MonthJournal(student=self.student, date=datetime.today())
        self.action = Action(action_detail='action detail',
                             model_name='model_name',
                             model_verbose_name='model_verbose_name')


    def test_student_unicode(self):
        self.assertEqual(unicode(self.student), u'Demo Student')

    def test_group_unicode(self):
        # test without leader
        self.assertEqual(unicode(self.group), u'Title')

        # test with leader
        self.assertEqual(unicode(self.group1), u'Title (Demo Student)')

    def test_journal_unicode(self):
        self.assertEqual(unicode(self.journal), u'Student: %d, %d' % (
            datetime.today().month,
            datetime.today().year))

    def test__action_unicode(self):
        self.assertEqual(unicode(self.action),
                    u'model_name (model_verbose_name)')
