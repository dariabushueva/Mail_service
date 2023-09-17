from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):
    """ Модель рассылки """

    CREATED = 'created'
    LAUNCHED = 'launched'
    COMPLETED = 'completed'

    STATUS_CHOICES = [
        (CREATED, 'Создана'),
        (LAUNCHED, 'Запущена'),
        (COMPLETED, 'Завершена'),
    ]

    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

    FREQUENCY_CHOICES = [
        (DAILY, 'Раз в день'),
        (WEEKLY, 'Раз в неделю'),
        (MONTHLY, 'Раз в месяц')
    ]

    topic = models.CharField(max_length=100, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Текст письма')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')

    status = models.CharField(max_length=10, verbose_name='Статус', default='created', choices=STATUS_CHOICES)
    start_time = models.DateTimeField(verbose_name='Начало рассылки')
    frequency = models.CharField(max_length=50, verbose_name='Периодичность', default='daily', choices=FREQUENCY_CHOICES)

    client = models.ManyToManyField('Client', blank=True, verbose_name='Клиент')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return f'{self.topic} ({self.status} - {self.start_time})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            (
                'set_status',
                'Can change status'
            )
        ]


class Client(models.Model):
    """ Модель клиента сервиса """

    email = models.EmailField(verbose_name='E-mail')
    name = models.CharField(max_length=150, verbose_name='Имя')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return f'{self.email} ({self.comment})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailingLogs(models.Model):
    """ Модель логов рассылки """

    last_attempt = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')
    attempt_status = models.CharField(max_length=50, verbose_name='Статус попытки')
    mail_server_response = models.BooleanField(verbose_name='Ответ почтового сервера')

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')

    def __str__(self):
        return f'{self.mailing} - {self.client} ({self.attempt_status} - {self.mail_server_response})'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'

