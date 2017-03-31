from django.core.management.base import BaseCommand, CommandError

from filings.services.get_filings import GetFilings

class Command(BaseCommand):
    help = 'Gets all the filings for a given proceeding'

    def add_arguments(self, parser):
        parser.add_argument('proceeding_name', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write("Starting getfilings command...")

        proceeding_name = options['proceeding_name']

        self.stdout.write("Pretending to find filings for proceeding {}".format(proceeding_name))

        get_filings = GetFilings('12-375')

        get_filings.perform()

        self.stdout.write("Finishing getfilings command.")
