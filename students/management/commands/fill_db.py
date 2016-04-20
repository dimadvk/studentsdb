from optparse import  make_option
from random import randrange

from django.utils import timezone
from django.core.management import BaseCommand
from django.contrib.auth.models import User

from students.models import Student, Group


class Command(BaseCommand):

    args = '<--group=NUM --student=NUM --user=NUM>'
    help = '''
        Creates specified number of objects with random parameters.
        Number must be in range 1..99.
        '''

    models = (('student', Student), ('group', Group), ('user', User))

    option_list = BaseCommand.option_list + (
        make_option('--student',
                    action='store',
                    dest='student',
                    help='Count of "student" objects',
                    ),
        make_option('--group',
                    action='store',
                    dest='group',
                    help='Count of "group" objects',
                    ),
        make_option('--user',
                    action='store',
                    dest='user',
                    help='Count of "user" objects',
                    ),
    )

    def handle(self, *args, **options):
        # checking here: 0 < count < 100, count of object is integer
        for name, model in self.models:
            if options.get(name) != None:
                count = options[name]
                try:
                    count = int(count)
                except:
                    raise ValueError("Number of '%s' objects must be an integer!"
                                     % name)
                if not 0< count <100:
                    raise ValueError("Number of '%s' objects must be in range 1..99!"
                                     % name)

        for name, model in self.models:
            if options[name]:
                count = int(options[name])
                while count > 0:
                    self._add_object_to_db(name)
                    count -= 1

    def _random_value(self, value=''):
        return value + str(randrange(10000))

    def _add_object_to_db(self, name):
        if name == 'student':
            student = Student(
                first_name=self._random_value('first_name'),
                last_name=self._random_value('last_name'),
                ticket=self._random_value(),
                birthday=timezone.now(),
            )
            student.save()
        if name == 'group':
            group = Group(
                title=self._random_value('title'),
                notes='note about group',
            )
            group.save()
        if name == 'user':
            user = User(
                username=self._random_value('username'),
                first_name=self._random_value('first_name'),
                last_name=self._random_value('last_name'),
                email=self._random_value("email") + '@example.com',
            )
            # User model have an unique field 'username'.
            # Generated 'username' can be not unique 
            #   in compare with existing objects.
            # In case of exception repeat creating object 'user'.
            try:
                user.save()
            except:
                self.add_object_to_db(name)
