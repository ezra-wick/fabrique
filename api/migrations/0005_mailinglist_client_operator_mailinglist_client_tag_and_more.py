# Generated by Django 4.0.3 on 2022-03-31 10:56

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_mailinglist_text_alter_client_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailinglist',
            name='client_operator',
            field=models.CharField(blank=True, max_length=10, verbose_name='Код мобильного оператора'),
        ),
        migrations.AddField(
            model_name='mailinglist',
            name='client_tag',
            field=models.CharField(blank=True, max_length=50, verbose_name='Тэг'),
        ),
        migrations.AlterField(
            model_name='client',
            name='operator_code',
            field=models.CharField(blank=True, max_length=10, verbose_name='Код мобильного оператора'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='text',
            field=models.CharField(blank=True, default=django.utils.timezone.now, max_length=500, verbose_name='Текст рассылки'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message',
            name='added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message',
            name='customer',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='message', to='api.client', verbose_name='Клиент'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message',
            name='mailing_list',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='message', to='api.mailinglist', verbose_name='Рассылка'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(blank=True, default=1, max_length=100, verbose_name='Статус отправки'),
            preserve_default=False,
        ),
    ]