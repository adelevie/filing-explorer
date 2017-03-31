import os
import json

from django.test import TestCase
from filings.services.get_filings import GetFilings

from unittest.mock import Mock, patch

from IPython import embed
import requests

class GetFilingsTestCase(TestCase):
    @patch('filings.services.get_filings.requests.get')
    def test_perform(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_json = json.loads(open(os.path.join('filings', 'fixtures', '12-375.json')).read())
        mock_get.return_value.json.return_value = mock_json

        proceeding_name = '12-375'
        api_key = os.environ.get('ECFS_API_KEY')

        get_filings = GetFilings(api_key, proceeding_name)
        filings_response = get_filings.perform()

        self.assertIs(filings_response.status_code, 200)

        filings_json = filings_response.json()

        self.assertTrue('filings' in filings_json.keys())

        filings = filings_json['filings']

        for filing in filings:
            proceedings = filing['proceedings']
            proceeding_names = []
            for proceeding in proceedings:
                proceeding_names.append(proceeding['name'])

            self.assertTrue(proceeding_name in proceeding_names)
