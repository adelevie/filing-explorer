import os
import json

from django.test import TestCase

from filings.services.get_filings import GetFilings
from filings.services.get_all_filings import GetAllFilings
from filings.services.save_filings import SaveFilings
from filings.services.filing_parser import FilingParser
from filings.services.get_open_calais_entities import GetOpenCalaisEntities
from filings.services.open_calais_parser import OpenCalaisParser
from filings.services.save_people import SavePeople

from filings.template_models import FilingTemplateModel

from .models import Filing, Person, Mention

from unittest.mock import Mock, patch

from IPython import embed
import requests

class FilingTemplateModelTestCase(TestCase):
    def test_basic(self):
        mock_filing = Mock()
        mock_filing.text = """
        Obama's Title II order has diminished broadband investment, stifled innovation, and left American consumers potentially on the hook for a new broadband tax.
        These regulations ended a decades-long bipartisan consensus that the Internet should be regulated through a light touch framework that worked better than anyone could have imagined and made the Internet what it is.
        For these reasons I urge you to fully repeal the Obama/Wheeler Internet regulations.
        """
        mock_filing.submission_type = "COMMENTS"
        mock_filing.filer = "Person C. Commenter"
        mock_filing.proceeding = "17-108"
        mock_filing.id = 1
        filing_view_template = FilingTemplateModel(mock_filing)

        self.assertIn("Obama's", filing_view_template.summary())
        self.assertIn(mock_filing.filer, filing_view_template.heading())
        self.assertIn(mock_filing.submission_type, filing_view_template.heading())
        self.assertIn(mock_filing.proceeding, filing_view_template.heading())
        self.assertEqual(filing_view_template.url_path(), "/filings/1/")

class SavePeopleTestCase(TestCase):
    @patch('filings.services.get_open_calais_entities.requests.post')
    def test_perform(self, mock_get):
        mock_text = open(os.path.join('filings', 'fixtures', 'calais.json')).read()
        mock_json = json.loads(mock_text)
        mock_response = Mock()
        mock_response.json.return_value = mock_json
        mock_response.text = mock_text
        mock_response.status_code = 200

        mock_get.return_value = mock_response

        text = """
        On July 28, 2016, Securus Technologies, Inc. ("Securus"),
        represented by Vice President and General Counsel Dennis J. Reinhold,
        Andrew J. Lipman, and the undersigned counsel, met with Travis Litman,
        Wireline Legal Advisor to Commissioner Jessica Rosenworcel,
        to discuss the Fact Sheet released in the above-named docket on July 24, 2016.
        """

        proceeding = '12-375'

        filing = Filing(
            proceeding=proceeding,
            proceedings=[proceeding],
            text=text,
            fcc_id='1234',
            submission_type='NOTICE OF EXPARTE',
            documents=[]
        )
        filing.save()

        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(Mention.objects.count(), 0)

        save_people = SavePeople('fakeApiKey', '12-375')
        save_people.perform()

        self.assertEqual(Person.objects.count(), 4)
        self.assertEqual(Mention.objects.count(), 4)


class OpenCalaisParserTestCase(TestCase):
    def test_names(self):
        calais_response = json.loads(open(os.path.join('filings', 'fixtures', 'calais.json')).read())

        parser = OpenCalaisParser(calais_response)

        names = parser.names()

        self.assertIs(names.__class__, list)

        expected = [
            'Andrew J. Lipman',
            'Dennis J. Reinhold',
            'Travis Litman',
            'Jessica Rosenworcel'
        ]
        self.assertEqual(names, expected)


class GetOpenCalaisEntitiesTestCase(TestCase):
    @patch('filings.services.get_open_calais_entities.requests.post')
    def test_perform(self, mock_get):
        mock_text = open(os.path.join('filings', 'fixtures', 'calais.json')).read()
        mock_json = json.loads(mock_text)
        mock_response = Mock()
        mock_response.json.return_value = mock_json
        mock_response.text = mock_text
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        text = """
        On July 28, 2016, Securus Technologies, Inc. ("Securus"),
        represented by Vice President and General Counsel Dennis J. Reinhold,
        Andrew J. Lipman, and the undersigned counsel, met with Travis Litman,
        Wireline Legal Advisor to Commissioner Jessica Rosenworcel,
        to discuss the Fact Sheet released in the above-named docket on July 24, 2016.
        """

        api_key = os.environ.get('OPEN_CALAIS_TOKEN')

        get_open_calais_entities = GetOpenCalaisEntities(api_key, text)
        get_open_calais_entities_response = get_open_calais_entities.perform()

        entities_dict = get_open_calais_entities_response.json()

        self.assertIs(entities_dict.__class__, dict)


class FilingParserTestCase(TestCase):
    def test_perform(self):
        filings_json = json.loads(open(os.path.join('filings', 'fixtures', '12-375-1.json')).read())

        filing_json = filings_json.get('filings')[0]

        filing_parser = FilingParser(filing_json)
        parsed_filing = filing_parser.perform()

        self.assertIn('proceeding', parsed_filing)
        self.assertIn('proceedings', parsed_filing)
        self.assertIn('text', parsed_filing)
        self.assertIn('fcc_id', parsed_filing)
        self.assertIn('contact_email', parsed_filing)
        self.assertIn('submission_type', parsed_filing)
        self.assertIn('filer', parsed_filing)
        self.assertIn('author', parsed_filing)
        self.assertIn('documents', parsed_filing)
        self.assertIn('date_submitted', parsed_filing)


class GetAllFilingsTestCase(TestCase):
    @patch('filings.services.get_filings.requests.get')
    def test_perform(self, mock_get):
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
