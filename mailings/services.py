import smtplib

from django.core.mail import send_mail
from datetime import datetime

from config import settings
from mailings.models import Mailing, MailingLogs


def send_mailings(mailing_item: Mailing):
    now = datetime.now()
    clients = mailing_item.client.all()

    for client in clients:
        attempt_status = ''
        sending_result = ''

        try:
            sending_result = send_mail(
                mailing_item.topic,
                mailing_item.body,
                settings.EMAIL_HOST_USER,
                [client.email],
                fail_silently=False,
            )

            if sending_result:
                attempt_status = 'Успешно'

        except smtplib.SMTPException as error:
            attempt_status = str(error)

        MailingLogs.objects.create(
            last_attempt=now,
            attempt_status=attempt_status,
            mail_server_response=sending_result,
            mailing=mailing_item,
            client=client,
        )


def check_sending():
    now = datetime.now()
    for ms in Mailing.objects.filter(status=Mailing.LAUNCHED):
        for mc in ms.client.all():
            ml = MailingLogs.objects.filter(client=mc, mailing=ms)
            if ml.exists():
                last_try = ml.order_by('-last_attempt').first()
                last_try_date = last_try.last_attempt.replace(tzinfo=None)
                if ms.DAILY:
                    if (now - last_try_date).days >= 1:
                        send_mailings(ms)
                        print(f'отправлено очередное ежедневное письмо {ms.topic}')
                if ms.WEEKLY:
                    if (now - last_try_date).days >= 7:
                        send_mailings(ms)
                        print(f'отправлено очередное еженедельное письмо {ms.topic}')
                if ms.MONTHLY:
                    if (now - last_try_date).days >= 30:
                        send_mailings(ms)
                        print(f'отправлено очередное ежемесячное письмо {ms.topic}')
            else:
                if now >= ms.start_time.replace(tzinfo=None):
                    send_mailings(ms)
                    print(f'отправлено новое письмо рассылки: {ms.topic}')

