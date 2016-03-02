import logging

from django.db.models.signals import post_save, post_delete, post_migrate
from django.dispatch import receiver, Signal

from .models import Student, Group, MonthJournal


@receiver(post_save, sender=Student)
def log_student_updated_added_event(sender, **kwargs):
    """Writes information about
        newly added or updated student into log file"""
    logger = logging.getLogger(__name__)

    student = kwargs['instance']
    if kwargs['created']:
        logger.info("Student added: %s %s (ID: %d)",
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

@receiver(post_delete, sender=Student)
def log_student_deleted_event(sender, **kwargs):
    logger = logging.getLogger(__name__)

    student = kwargs['instance']
    logger.info("Student deleted: %s %s (ID: %d)",
                student.first_name,
                student.last_name,
                student.id
               )

@receiver(post_save, sender=Group)
def log_group_updated_added_event(sender, **kwargs):
    logger = logging.getLogger(__name__)
    group = kwargs['instance']
    if kwargs['created']:
        logger.info("Group created: %s (Leader: %s) (ID: %d)",
                    group.title, group.leader, group.id
                   )
    else:
        logger.info("Group updated: %s (Leader: %s) (ID: %d)",
                   group.title, group.leader, group.id
                   )

@receiver(post_delete, sender=Group)
def log_group_deleted_event(sender, **kwargs):
    logger.logging.getLogger(__name__)
    group = kwargs['instance']
    logger.info("Group deleted: %s (ID: %d)", group.title, group.id)

@receiver(post_save, sender=MonthJournal)
def log_monthjournal_changes(sender, **kwargs):
    logger = logging.getLogger(__name__)
    monthjournal = kwargs['instance']
    logger.info("MonthJournal updated: %s (Journal ID: %d)",
                monthjournal.student,
                monthjournal.id
               )

# custom signal contact_admin
contact_admin_sent = Signal()

@receiver(contact_admin_sent)
def log_contact_admin(sender, **kwargs):
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
