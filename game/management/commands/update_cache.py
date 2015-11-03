from django.core.management.base import BaseCommand, CommandError

from slr1 import celery_app
from game.tasks import recalc_all


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        recalc_all.delay()
