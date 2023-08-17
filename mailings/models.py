from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):
    """ Рассылка """

    topic = models.CharField(max_length=100, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Текст письма')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')

    settings = models.ForeignKey('MailingSettings', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} - {self.topic}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingSettings(models.Model):
    """ Настройка рассылки """

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('launched', 'Запущена'),
        ('completed', 'Завершена'),
    ]
    FREQUENCY_CHOICES = [
        ('daily', 'Раз в день'),
        ('two_time_week', 'Два раза в неделю'),
        ('weekly', 'Раз в неделю'),
        ('two_time_month', 'Два раза в месяц'),
        ('monthly', 'Раз в месяц')
    ]

    status = models.CharField(max_length=10, verbose_name='Статус', default='created', choices=STATUS_CHOICES)
    start_time = models.DateTimeField(verbose_name='Начало рассылки')
    frequency = models.CharField(max_length=50, verbose_name='Периодичность', default='daily', choices=FREQUENCY_CHOICES)

    def __str__(self):
        return f'{self.pk} ({self.start_time} - {self.frequency})'

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'


class Client(models.Model):
    """ Клиент сервиса """

    email = models.EmailField(verbose_name='E-mail')
    name = models.CharField(max_length=150, verbose_name='Имя')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    mailings = models.ManyToManyField(Mailing, **NULLABLE)

    def __str__(self):
        return f'{self.email} ({self.name})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailingLogs(models.Model):
    """ Логи рассылки """

    last_attempt = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')
    attempt_status = models.CharField(max_length=50, verbose_name='Статус попытки')
    mail_server_response = models.TextField(**NULLABLE, verbose_name='Ответ почтового сервера')

    mailing_list = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')

    def __str__(self):
        return f'{self.mail_server_response} ({self.attempt_status} - {self.last_attempt})'

    class Meta:
        verbose_name = 'Логи рассылки'
        verbose_name_plural = 'Логи рассылки'
