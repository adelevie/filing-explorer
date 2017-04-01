import requests

from IPython import embed

class GetFilings(object):
    def __init__(self, api_key, proceeding_name, **kwargs):
        self._proceeding_name = proceeding_name
        self._api_key = api_key
        self._limit = str(kwargs.get('limit', 1000))
        self._offset = str(kwargs.get('offset', 0))

    def perform(self):
        payload = {
            'api_key': self._api_key,
            'proceedings.name': self._proceeding_name,
            'limit': self._limit,
            'offset': self._offset
        }
        url = 'https://publicapi.fcc.gov/ecfs/filings'

        filings_response = requests.get(url, params=payload)

        return filings_response
