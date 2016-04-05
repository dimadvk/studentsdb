from django.core.management import BaseCommand
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from students.models import Student, Group


class Command(BaseCommand):
    args = '<model_name model_name ...>'
    help = _(u"Prints to console number of student realted objects in a database.")

    models = (('student', Student), ('group', Group), ('user', User))

    def handle(self, *args, **options):
        for name, model in self.models:
            if name in args:
                self.stdout.write(_(u'Number of %(name)ss in database: %(count)d') %
                                  (name, model.objects.count()))

#        if 'student' in args:
#            self.stdout.write('Number of students in database: %d' % 
#                              Student.objects.count())
#        if 'group' in args:
#            self.stdout.write('Number of groups in database: %d' % 
#                              Group.objects.count())
#        if 'user' in args:
#            self.stdout.write('Number of users in database: %d' % 
#                              User.objects.count())
