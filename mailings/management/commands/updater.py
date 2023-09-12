from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import BaseCommand

from mailings.services import check_sending


class Command(BaseCommand):

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_job(check_sending, 'interval', seconds=30)
        scheduler.start()

