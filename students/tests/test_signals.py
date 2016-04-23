import logging
from datetime import datetime

from django.utils.six import StringIO
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from students.models import Student, Group, MonthJournal


class StudentSignalsTests(TestCase):

    fixtures = ['students_test_data.json']

    def test_log_student_updated_added_event(self):
        """Check logging signal for newly created student"""
        # add own root handler to catch student signals output
        out = StringIO()
        handler = logging.StreamHandler(out)
        logging.root.addHandler(handler)

        # now create student, this should raise new message inside
        # our logger output file
        student = Student(first_name='Demo', last_name='Student', ticket='123')
        student.save()

        # check output file content
        out.seek(0)
        self.assertEqual(out.readlines()[-1],
             'Student added: Demo Student (ID: %d)\n' % student.id)

        # now update existing student and check last line in out
        student.ticket = '12345'
        student.save()
        out.seek(0)
        self.assertEqual(out.readlines()[-1],
             'Student updated: Demo Student (ID: %d)\n' % student.id)

        # remove our handler from root logger
        logging.root.removeHandler(handler)

    def test_log_student_deleted_event(self):
        """Check logging signal for deleted student"""
        # add own root handler to catch student signals output
        out = StringIO()
        handler = logging.StreamHandler(out)
        logging.root.addHandler(handler)

        # now create and delete student, this should raise new message inside
        # our logger output file
        student = Student(first_name='Demo', last_name='Student', ticket='123')
        student.save()
        student_id = student.id
        student.delete()

        # check output file content
        out.seek(0)
        self.assertEqual(out.readlines()[-1],
             'Student deleted: Demo Student (ID: %d)\n' % student_id)

        # remove our handler from root logger
        logging.root.removeHandler(handler)

    def test_log_group_updated_added_event(self):
        """Check logging signal for newly created group"""
        # add own root handler to catch group signals output
        out = StringIO()
        handler = logging.StreamHandler(out)
        logging.root.addHandler(handler)

        # now create group, this should raise new message inside
        # our logger output file
        group = Group(title='Demo Group')
        group.save()

        # check output file content
        out.seek(0)
        self.assertEqual(out.readlines()[-1],
             "Group created: Demo Group (ID: %d)\n" % group.id)

        # now update existing student and check last line in out
        group.notes = 'some group note'
        group.save()
        out.seek(0)
        self.assertEqual(out.readlines()[-1],
             "Group updated: Demo Group (ID: %d)\n" % group.id)

        # remove our handler from root logger
        logging.root.removeHandler(handler)

    def test_log_group_deleted_event(self):
        """Check logging signal for deleted group"""
        # add own root handler to catch group signals output
        out = StringIO()
        handler = logging.StreamHandler(out)
        logging.root.addHandler(handler)

        # now create and delete group, this should raise new message inside
        # our logger output file
        group = Group(title='Demo Group')
        group.save()
        group_id = group.id
        group.delete()

        # check output file content
        out.seek(0)
        self.assertEqual(out.readlines()[-1],
             "Group deleted: Demo Group (ID: %d)\n" % group_id)

        # remove our handler from root logger
        logging.root.removeHandler(handler)

    def test_log_monthjournal_changes(self):
        """Test logging signal for changes in monthjournal"""
         # add own root handler to catch group signals output
        out = StringIO()
        handler = logging.StreamHandler(out)
        logging.root.addHandler(handler)

        student, created = Student.objects.get_or_create(
            first_name='Demo', last_name='Student', ticket='123')
        monthjournal, created = MonthJournal.objects.get_or_create(
            student=student, date=datetime.today())
        monthjournal.present_day1 = True

        # check output file content
        out.seek(0)
        self.assertEqual(out.readlines()[-1],
             "MonthJournal updated: Demo Student (Journal ID: %d)\n"
                         % monthjournal.id)

        # remove our handler from root logger
        logging.root.removeHandler(handler)

    def test_log_contact_admin(self):
        """Test log message when mail was sent"""
        # add own root handler to catch group signals output
        out = StringIO()
        handler = logging.StreamHandler(out)
        logging.root.addHandler(handler)

        # prepare client and login as administrator
        client = Client()
        client.login(username='admin', password='admin')

        # make form submit
        client.post(reverse('contact_admin'), {
            'from_email': 'from@gmail.com',
            'subject': 'test email',
            'message': 'test email message',
        })
        # check log message
        out.seek(0)
        self.assertIn("A message via Contact Form was sent",
                      out.readlines()[-1])

        # remove our handler from root logger
        logging.root.removeHandler(handler)

