import os
from django.test import TestCase

from filings.services.get_filings import GetFilings

from IPython import embed

class GetFilingsTestCase(TestCase):
    def test_perform(self):
        proceeding_name = '12-375'
        api_key = os.environ.get('ECFS_API_KEY')

        get_filings = GetFilings(api_key, proceeding_name)
        filings = get_filings.perform()

        self.assertIs(filings.__class__, list)
