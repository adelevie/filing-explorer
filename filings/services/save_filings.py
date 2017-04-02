from filings.models import Filing
from filings.services.filing_parser import FilingParser


from IPython import embed

class SaveFilings(object):
    def __init__(self, filings):
        self._filings = filings

    def perform(self):
        for filing_json in self._filings:
            filing_parser = FilingParser(filing_json)
            filing_data = filing_parser.perform()
            fcc_id = filing_data.get('fcc_id')

            try:
                filing = Filing.objects.get(fcc_id=fcc_id)
            except Filing.DoesNotExist:
                filing = Filing(**filing_data)

            try:
                filing.save()
            except:
                print("Error saving filing: {}".format(fcc_id))
