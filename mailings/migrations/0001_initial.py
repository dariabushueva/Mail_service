# Generated by Django 4.2.4 on 2023-08-19 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=100, verbose_name='Тема письма')),
                ('body', models.TextField(verbose_name='Текст письма')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
                ('status', models.CharField(choices=[('created', 'Создана'), ('launched', 'Запущена'), ('completed', 'Завершена')], default='created', max_length=10, verbose_name='Статус')),
                ('start_time', models.DateTimeField(verbose_name='Начало рассылки')),
                ('frequency', models.CharField(choices=[('daily', 'Раз в день'), ('weekly', 'Раз в неделю'), ('monthly', 'Раз в месяц')], default='daily', max_length=50, verbose_name='Периодичность')),
                ('client', models.ManyToManyField(blank=True, to='mailings.client', verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
        migrations.CreateModel(
            name='MailingLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_attempt', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')),
                ('attempt_status', models.CharField(max_length=50, verbose_name='Статус попытки')),
                ('mail_server_response', models.TextField(blank=True, null=True, verbose_name='Ответ почтового сервера')),
                ('client', models.ManyToManyField(blank=True, null=True, to='mailings.client', verbose_name='Клиент')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailings.mailing', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Логи',
            },
        ),
    ]
