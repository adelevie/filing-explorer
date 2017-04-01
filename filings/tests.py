import os
import json

from django.test import TestCase

from filings.services.get_filings import GetFilings
from filings.services.get_all_filings import GetAllFilings
from filings.services.save_filings import SaveFilings

from .models import Filing

from unittest.mock import Mock, patch

from IPython import embed
import requests

class GetAllFilingsTestCase(TestCase):
    @patch('filings.services.get_filings.requests.get')
    def test_perform(self, mock_get):
        mock_get.status_code.return_value = 200

        json1 = json.loads(open(os.path.join('filings', 'fixtures', '12-375-1.json')).read())
        json2 = json.loads(open(os.path.join('filings', 'fixtures', '12-375-2.json')).read())

        mock_response = Mock()
        mock_response.status_code = 200

        mock_response.json.side_effect = [json1, json1, json2]

        mock_get.return_value = mock_response

        proceeding_name = '12-375'
        api_key = 'aFakeApiKey'

        get_all_filings = GetAllFilings(api_key, proceeding_name, increment=10)
        filings = get_all_filings.perform()

        # 20 is the hardcoded filing length in the 'aggregations' section
        # of the json fixtures. Each fixture has 10 filings, there are two fixtures.
        self.assertEqual(len(filings), 20)

class GetFilingsTestCase(TestCase):
    def test_init(self):
        proceeding_name = '12-375'
        api_key = 'aFakeApiKey'

        get_filings = GetFilings(api_key, proceeding_name, limit=10, offset=10)

    @patch('filings.services.get_filings.requests.get')
    def test_perform(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_json = json.loads(open(os.path.join('filings', 'fixtures', '12-375-1.json')).read())
        mock_get.return_value.json.return_value = mock_json

        proceeding_name = '12-375'
        api_key = 'aFakeApiKey'

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

class SaveFilingsTestCase(TestCase):
    def test_perform(self):
        filings_json = json.loads(open(os.path.join('filings', 'fixtures', '12-375-1.json')).read())

        filings = filings_json['filings']

        self.assertEqual(Filing.objects.count(), 0)

        save_filings = SaveFilings(filings)
        save_filings.perform()

        self.assertEqual(Filing.objects.count(), len(filings))

        queried_filings = Filing.objects.all()

        for queried_filing in queried_filings:
            self.assertTrue(queried_filing.proceeding is not None)

        # test for idempotency:
        # if the filings have already been scraped, update the object,
        # but don't save a new one.

        filings = filings_json['filings']

        save_filings = SaveFilings(filings)
        save_filings.perform()

        self.assertEqual(Filing.objects.count(), len(filings))
