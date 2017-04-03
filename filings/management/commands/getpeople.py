import os

from django.core.management.base import BaseCommand, CommandError

from filings.services.save_people import SavePeople

from IPython import embed

class Command(BaseCommand):
    help = 'Gets all the people mentioned in filings that are already saved in the database'

    def add_arguments(self, parser):
        parser.add_argument('proceeding_name', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write("Starting getpeople command...")

        proceeding_name = options['proceeding_name'][0]

        self.stdout.write("Retreiving people for filings in for proceeding {}".format(proceeding_name))

        save_people = SavePeople(os.environ.get('OPEN_CALAIS_TOKEN'), '12-375')
        save_people.perform()

        self.stdout.write("Finishing getpeople command.")
