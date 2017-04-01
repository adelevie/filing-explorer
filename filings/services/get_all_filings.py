from filings.services.get_filings import GetFilings

from IPython import embed

class GetAllFilings(object):
    def __init__(self, api_key, proceeding_name, **kwargs):
        self._api_key = api_key
        self._proceeding_name = proceeding_name
        self._increment = kwargs.get('increment', 1000)

    def perform(self):
        get_filings = GetFilings(self._api_key,
                                 self._proceeding_name,
                                 offset=0,
                                 limit=self._increment)

        filings_response = get_filings.perform()

        buckets = filings_response.json() \
                    .get('aggregations') \
                    .get('proceedings_name') \
                    .get('buckets')

        filings_count = None
        for bucket in buckets:
            if bucket.get('key') == self._proceeding_name:
                filings_count = bucket.get('doc_count')

        offsets = list(range(0, filings_count, self._increment))

        responses = []
        for offset in offsets:
            get_filings = GetFilings(self._api_key,
                                     self._proceeding_name,
                                     offset=offset,
                                     limit=self._increment)
            response = get_filings.perform()
            responses.append(response)


        all_filings = []

        for response in responses:
            filings = response.json().get('filings')
            for filing in filings:
                all_filings.append(filing)

        return all_filings
