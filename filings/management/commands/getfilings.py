import os

from django.core.management.base import BaseCommand, CommandError

from filings.services.get_filings import GetFilings
from filings.services.save_filings import SaveFilings

class Command(BaseCommand):
    help = 'Gets all the filings for a given proceeding'

    def add_arguments(self, parser):
        parser.add_argument('proceeding_name', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write("Starting getfilings command...")

        proceeding_name = options['proceeding_name']

        self.stdout.write("Retriving filings for proceeding {}".format(proceeding_name))

        get_filings = GetFilings(os.environ.get('ECFS_API_KEY'), proceeding_name)

        filings_json = get_filings.perform().json()

        save_filings = SaveFilings(filings_json)

        save_filings.perform()

        self.stdout.write("Finishing getfilings command.")
