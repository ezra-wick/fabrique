from rest_framework import serializers

from .models import Client, MailingList, Message


class ClientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'phone', 'operator_code', 'tag', 'client_timezone',)


class MailingSerializers(serializers.ModelSerializer):

    class Meta:
        model = MailingList
        fields = (
            'id',
            'mailing_start',
            'mailing_end',
            'text',
            'client_operator',
            'client_tag',
            'job_id'
            )
        read_only_fields = ('job_id',)


class MessageSerializers(serializers.ModelSerializer):
    client_phone = serializers.IntegerField()

    class Meta:
        model = Message
        fields = (
            'id',
            'client_phone',
            'customer',
            'mailing_list',
            'added',
            'message',
            'send_time',
            'status',
            )
        read_only_fields = (
            'customer',
            'mailing_list',
            'send_time',
            'status',
            'added',
            )


class SendMessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'customer',
            'mailing_list',
            'added',
            'message',
            'send_time',
            'status',
            )
        read_only_fields = (
            'customer',
            'mailing_list',
            'send_time',
            'status',
            'added',
            )
