import requests

from IPython import embed

class GetFilings(object):
    def __init__(self, api_key, proceeding_name):
        self._proceeding_name = proceeding_name
        self._api_key = api_key

    def perform(self):
        print('pretending to get the filings from proceeding {}!!!!'.format(self._proceeding_name))

        payload = {
            'q': self._proceeding_name,
            'limit': '10',
            'api_key': self._api_key
        }
        url = 'https://publicapi.fcc.gov/ecfs/filings'

        filings_response = requests.get(url, params=payload)

        filings = filings_response.json()['filings']

        return filings
