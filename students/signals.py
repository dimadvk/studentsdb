import logging

from django.db.models.signals import post_save, post_delete, post_migrate
from django.core.signals import request_started
from django.dispatch import receiver, Signal

from .models import Student, Group, MonthJournal, Action


#@receiver(post_save)
#def test(sender, **kwargs):
#    import ipdb; ipdb.set_trace()
#    pass


@receiver(post_save, sender=Student)
def log_student_updated_added_event(sender, **kwargs):
    """Writes information about
        newly added or updated student into log file"""
    logger = logging.getLogger(__name__)
    action = Action()

    student = kwargs['instance']
    if kwargs['created']:
        logger.info("Student added: %s %s (ID: %d)",
                    student.first_name,
                    student.last_name,
                    student.id
                   )
        action.action_detail = "Student added: %s %s (ID: %d)" % (
            student.first_name,
            student.last_name,
            student.id
            )
    else:
        logger.info("Student updated: %s %s (ID: %d)",
                    student.first_name,
                    student.last_name,
                    student.id
                   )
        action.action_detail = "Student updated: %s %s (ID: %d)" % (
            student.first_name,
            student.last_name,
            student.id
            )
    action.model_name = sender.__name__
    action.model_verbose_name = u"Student"
    action.save()



@receiver(post_delete, sender=Student)
def log_student_deleted_event(sender, **kwargs):
    """Log message when studetn object got deleted"""
    logger = logging.getLogger(__name__)
    action = Action()

    student = kwargs['instance']
    logger.info("Student deleted: %s %s (ID: %d)",
                student.first_name,
                student.last_name,
                student.id
               )
    action.action_detail = "Student deleted: %s %s (ID: %d)" % (
        student.first_name,
        student.last_name,
        student.id,
        )
    action.model_name = sender.__name__
    action.model_verbose_name = u"Student"
    action.save()


@receiver(post_save, sender=Group)
def log_group_updated_added_event(sender, **kwargs):
    """Log message when group got updated or added new one"""
    logger = logging.getLogger(__name__)
    action = Action()

    group = kwargs['instance']
    if kwargs['created']:
        logger.info("Group created: %s (ID: %d)",
                    group.title, group.id
                   )
        action.action_detail = "Group created: %s (ID: %d)" % (
            group.title, group.id,
        )
    else:
        logger.info("Group updated: %s (ID: %d)",
                    group.title, group.id
                   )
        action.action_detail = "Group updated: %s (ID: %d)" % (
            group.title, group.id,
        )
    action.model_name = sender.__name__
    action.model_verbose_name = u"Group"
    action.save()


@receiver(post_delete, sender=Group)
def log_group_deleted_event(sender, **kwargs):
    """Log message when group object got deleted"""
    logger = logging.getLogger(__name__)
    action = Action()
    group = kwargs['instance']
    logger.info("Group deleted: %s (ID: %d)", group.title, group.id)
    action.action_detail = "Group deleted: %s (ID: %d)" % (group.title, group.id)
    action.model_name = sender.__name__
    action.model_verbose_name = u"Group"
    action.save()

@receiver(post_save, sender=MonthJournal)
def log_monthjournal_changes(sender, **kwargs):
    """Log message when monthjournal object got changed"""
    logger = logging.getLogger(__name__)
    action = Action()
    monthjournal = kwargs['instance']
    logger.info("MonthJournal updated: %s (Journal ID: %d)",
                monthjournal.student,
                monthjournal.id
               )
    action.action_detail = "MonthJournal updated: %s (Journal ID: %d)" % (
        monthjournal.student,
        monthjournal.id,
    )
    action.model_name = sender.__name__
    action.model_verbose_name = u"Journal"
    action.save()
    print kwargs


# custom signal contact_admin
contact_admin_sent = Signal()

@receiver(contact_admin_sent)
def log_contact_admin(sender, **kwargs):
    """Log message when message to admin got sent"""
    logger = logging.getLogger(__name__)
    logger.info('A message via Contact Form was sent. Sender: %s; Subject: %s',
                kwargs['message_sender'],
                kwargs['message_subject'],
               )

@receiver(post_migrate)
def log_migrate(sender, **kwargs):
    logger = logging.getLogger(__name__)
    logger.info('Migration done. Application: "%s". Using database: %s',
                kwargs['app_config'].label,
                kwargs['using'],
               )

# requests counter
REQUESTS_COUNT = 0
@receiver(request_started)
def count_requests(sender, *args, **kwargs):
    global REQUESTS_COUNT
    REQUESTS_COUNT += 1
