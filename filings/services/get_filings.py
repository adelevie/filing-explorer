import requests

from IPython import embed

class GetFilings(object):
    def __init__(self, api_key, proceeding_name):
        self._proceeding_name = proceeding_name
        self._api_key = api_key

    def perform(self):
        payload = {
            'api_key': self._api_key,
            'proceedings.name': self._proceeding_name,
            'limit': '1000',
            'offset': '0'
        }
        url = 'https://publicapi.fcc.gov/ecfs/filings'

        filings_response = requests.get(url, params=payload)

        return filings_response
