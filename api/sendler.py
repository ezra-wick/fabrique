
import logging
import os

import requests
from django.utils import timezone
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

bearer_token = os.getenv('bearer_token')

headers = {
    "Authorization": f"Bearer {bearer_token}"
    }


def send_message(msg_id, phone, text):
    endpoint = f"https://probe.fbrq.cloud/v1/send/{msg_id}"
    params = {
        "id": msg_id,
        "phone": phone,
        "text": text
    }
    return requests.post(endpoint, json=params, headers=headers).json()


def send_messages(Client, Message, instance):
    clients = Client.objects.filter(
        operator_code=instance.client_operator,
        tag=instance.client_tag
        )

    text = instance.text
    instance.save()
    for client in clients:

        message = Message.objects.create(
            customer=client,
            mailing_list=instance,
            message=text,
        )
        logger.info(f'clietns_id: {client.id}, message_id: {message.id}')
        status = send_message(message.id, client.phone, text)['message']
        if status:
            message.status = status
            logger.info(f'message_status: {message.status}')
        else:
            message.status = 'FAIL'
        message.send_time = timezone.now()
        message.save()


if __name__ == "__main__":
    pass
