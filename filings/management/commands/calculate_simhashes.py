import os

from django.core.management.base import BaseCommand, CommandError

from filings.models import Filing

from IPython import embed

from simhash import Simhash
import re

def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

class Command(BaseCommand):
    help = 'Calculates and saves simhashes for all filings'

    def add_arguments(self, parser):
        parser.add_argument('proceeding_name', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write("Starting calculate_simhashes command...")

        proceeding_name = options['proceeding_name'][0]

        self.stdout.write("Calculating simhashes for proceeding {}".format(proceeding_name))

        # find all filings in the docket that lack a simhash
        filings = Filing.objects \
                    .filter(simhash=None, proceeding=proceeding_name) \
                    .all()

        counter = len(filings)

        for filing in filings:
            if filing.text:
                sh = Simhash(get_features(filing.text)).value
                filing.simhash = sh
                filing.save()
                print("Added simhash ({}) to filing (id: {})".format(sh, filing.pk))
                print("{} filings left to compute".format(counter))
                counter = counter - 1

        self.stdout.write("Finishing calculate_simhashes command.")
