from django.db.models.signals import pre_save
from django.utils import timezone

from .models import Client, MailingList, Message
from .scheduler import add_job, modify_job
from .sendler import send_messages


def send_mailing_status(sender, instance, **kwargs):
    if instance.pk:
        if instance.mailing_start >= timezone.now() <= instance.mailing_end:
            modify_job(
                instance.mailing_start,
                instance.job_id,
                Client,
                Message,
                instance
                )
    else:
        if instance.mailing_start >= timezone.now() <= instance.mailing_end:
            instance.job_id = add_job(
                send_messages,
                instance.mailing_start,
                Client,
                Message,
                instance
                )


pre_save.connect(send_mailing_status, sender=MailingList)
