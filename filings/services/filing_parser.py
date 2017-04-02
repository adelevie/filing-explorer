from IPython import embed

class FilingParser(object):
    def __init__(self, filing):
        self._filing = filing

    def perform(self):
        filing = {}

        filing['fcc_id'] = self._filing.get('id_submission', None)
        filing['contact_email'] = self._filing.get('contact_email', None)
        filing['filer'] = self._filing.get('filers', [])[0].get('name')
        filing['author'] = self._author()
        filing['submission_type'] = self._filing.get('submissiontype', {}).get('description', None)
        filing['documents'] = self._documents()
        filing['proceeding'] = self._proceeding()
        filing['proceedings'] = self._proceedings()
        filing['text'] = self._filing.get('text_data', None)
        filing['date_submitted'] = self._filing.get('date_submission', None)

        return filing

    def _documents(self):
        documents = []
        for document in self._filing.get('documents', []):
            documents.append(document.get('src'))
        return documents

    def _author(self):
        author = None
        authors = self._filing.get('authors', None)
        if authors:
            author = authors[0].get('name')
        return author

    def _proceeding(self):
         return self._filing['proceedings'][0].get('name')

    def _proceedings(self):
        proceedings_json = self._filing['proceedings']
        proceedings = []
        for p in proceedings_json:
            proceedings.append(p.get('name'))
        return proceedings
