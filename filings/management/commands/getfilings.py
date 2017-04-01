import os

from django.core.management.base import BaseCommand, CommandError

from filings.services.get_all_filings import GetAllFilings
from filings.services.save_filings import SaveFilings

from IPython import embed

class Command(BaseCommand):
    help = 'Gets all the filings for a given proceeding'

    def add_arguments(self, parser):
        parser.add_argument('proceeding_name', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write("Starting getfilings command...")

        proceeding_name = options['proceeding_name'][0]

        self.stdout.write("Retreiving filings for proceeding {}".format(proceeding_name))

        get_filings = GetAllFilings(os.environ.get('ECFS_API_KEY'), proceeding_name)

        filings = get_filings.perform()

        save_filings = SaveFilings(filings)

        save_filings.perform()

        self.stdout.write("Finishing getfilings command.")
