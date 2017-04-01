from filings.models import Filing

from IPython import embed

class SaveFilings(object):
    def __init__(self, filings):
        self._filings = filings

    def perform(self):
        for filing_json in self._filings:

            proceedings_json = filing_json['proceedings']

            proceedings = []
            for p in proceedings_json:
                proceedings.append(p.get('name'))

            proceeding = proceedings_json[0].get('name')

            author = None
            authors = filing_json.get('authors', None)
            if authors:
                author = authors[0].get('name')

            documents = []
            for document in filing_json.get('documents', []):
                documents.append(document.get('src'))

            fcc_id = filing_json.get('id_submission', None)

            try:
                filing = Filing.objects.get(fcc_id=fcc_id)
            except Filing.DoesNotExist:
                filing = Filing()
                filing.fcc_id = fcc_id
                filing.contact_email = filing_json.get('contact_email', None)
                filing.filer = filing_json.get('filers', [])[0].get('name')
                filing.author = author
                filing.submission_type = filing_json.get('submissiontype', {}).get('description', None)
                filing.documents = documents
                filing.proceeding = proceeding
                filing.proceedings = proceedings
                filing.text = filing_json.get('text_data', None)
                filing.date_submitted = filing_json.get('date_submission', None)

            try:
                filing.save()
            except:
                print("Error saving filing")
