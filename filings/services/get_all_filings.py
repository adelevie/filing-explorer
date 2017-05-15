from filings.services.get_filings import GetFilings
from filings.services.save_filings import SaveFilings
from IPython import embed

class GetAllFilings(object):
    def __init__(self, api_key, proceeding_name, **kwargs):
        self._api_key = api_key
        self._proceeding_name = proceeding_name
        self._increment = kwargs.get('increment', 10000)

    def perform(self):
        get_filings = GetFilings(self._api_key,
                                 self._proceeding_name,
                                 offset=0,
                                 limit=self._increment)

        print("Starting query for proceeding {}, offset {}, limit {}".format(self._proceeding_name, 0, self._increment))
        filings_response = get_filings.perform()
        print("Finishing query for proceeding {}, offset {}, limit {}".format(self._proceeding_name, 0, self._increment))

        buckets = filings_response.json() \
                    .get('aggregations') \
                    .get('proceedings_name') \
                    .get('buckets')

        filings_count = None
        for bucket in buckets:
            if bucket.get('key') == self._proceeding_name:
                filings_count = bucket.get('doc_count')

        offsets = list(range(0, filings_count, self._increment))

        for offset in offsets:
            get_filings = GetFilings(self._api_key,
                                     self._proceeding_name,
                                     offset=offset,
                                     limit=self._increment)

            print("Starting query for proceeding {}, offset {}, limit {}".format(self._proceeding_name, offset, self._increment))
            response = get_filings.perform()
            filings = response.json().get('filings')

            print("-------About to save {} filings".format(len(filings)))
            save_filings = SaveFilings(filings)
            save_filings.perform()
            print("-------Saved {} filings".format(len(filings)))

            print("Finishing query for proceeding {}, offset {}, limit {}".format(self._proceeding_name, offset, self._increment))
