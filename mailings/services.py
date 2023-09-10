import smtplib

from django.core.mail import send_mail
from datetime import datetime

from config import settings
from mailings.models import Mailing, MailingLogs, Client


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

#ms = Mailing.objects.filter(status=Mailing.LAUNCHED)
#mf = Mailing.objects.filter(frequency=Mailing.WEEKLY)


def check_sending():
    now = datetime.now()
    for ms in Mailing.objects.filter(status=Mailing.LAUNCHED):
        for mc in ms.mailingclient_set.all():
            ml = MailingLogs.objects.filter(client=mc.client, mailing=ms)
            if ml.exists():
                last_try_date = ml.order_by('-last_attempt').first()
                if ms.frequency == Mailing.frequency.DAILY:
                    if (now - last_try_date).days >= 1:
                        send_mailings(ms)
                if ms.frequency == Mailing.frequency.WEEKLY:
                    if (now - last_try_date).days >= 7:
                        send_mailings(ms)
                if ms.frequency == Mailing.frequency.MONTHLY:
                    if (now - last_try_date).days >= 30:
                        send_mailings(ms)
            else:
                send_mailings(ms)
                print('sent it')




