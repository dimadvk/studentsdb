import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

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
