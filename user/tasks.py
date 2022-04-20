from __future__ import absolute_import, unicode_literals


from celery import shared_task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from .emails import send_welcome_email

@shared_task(name='send_welcome_email_task')
def send_welcome_email_task(token):
    logger.info('Welcome email sent')
    return send_welcome_email(token)