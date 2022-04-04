import pytz
from django.core.validators import RegexValidator
from django.db import models

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class Client(models.Model):
    phone_regex = RegexValidator(
        regex=r'^7\d{9,10}$',
        message="Номер телефона должен быть в формате 7XXXXXXXXXX \
                (X - цифра от 0 до 9)"
        )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=11,
        blank=True,
        verbose_name='Телефон',
        unique=True
        )
    operator_code = models.CharField(
        max_length=10,
        blank=True,
        verbose_name='Код мобильного оператора'
        )
    tag = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Тэг'
        )
    client_timezone = models.CharField(
        max_length=32,
        blank=True,
        verbose_name='Часовой пояс'
        )


class MailingList(models.Model):
    added = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        verbose_name='Дата создания',
        )
    mailing_start = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Начало рассылки',
        )
    mailing_end = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Окончание рассылки',
        )
    text = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Текст рассылки'
        )
    client_operator = models.CharField(
        max_length=10,
        blank=True,
        verbose_name='Код мобильного оператора'
        )
    client_tag = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Тэг'
        )
    job_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Номер работы планировщика'
        )


class Message(models.Model):
    customer = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='message',
        verbose_name='Клиент',
        null=True,
        blank=True,
        )

    mailing_list = models.ForeignKey(
        MailingList,
        on_delete=models.CASCADE,
        related_name='message',
        verbose_name='Рассылка',
        null=True,
        blank=True,
        )
    added = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        verbose_name='Дата создания',
        )
    send_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Время отправки',
        )
    message = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name='Текст сообщения'
        )
    status = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Статус отправки'
        )
