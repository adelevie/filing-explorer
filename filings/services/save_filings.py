from filings.models import Proceeding, Filing

from IPython import embed

class SaveFilings(object):
    def __init__(self, filings_json):
        self._filings_json = filings_json

    def perform(self):
        filings = self._filings_json['filings']

        filing_insertions = []

        for filing in filings:
            proceeding_json = filing['proceedings'][0]

            proceeding, created = Proceeding.objects.get_or_create(
                name=proceeding_json.get('name', None),
                bureau_name=proceeding_json.get('bureau_name', None),
                bureau_code=proceeding_json.get('bureau_code', None),
                fcc_id=proceeding_json.get('id_proceeding', None),
                description=proceeding_json.get('description', None),
            )

            filing_insertion = Filing(
                proceeding=proceeding,
                text=filing.get('text_data', None),
                fcc_id=filing.get('id_submission', None),
                contact_email=filing.get('contact_email', None),
                filer=filing.get('filers', [])[0]
            )

            filing_insertions.append(filing_insertion)

        Filing.objects.bulk_create(filing_insertions)
