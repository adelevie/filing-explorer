import requests

from IPython import embed

class GetOpenCalaisEntities(object):
    def __init__(self, api_key, text):
        self._api_key = api_key
        self._text = text

    def perform(self):
        headers = {
            'X-AG-Access-Token' : self._api_key,
            'Content-Type' : 'text/raw',
            'outputFormat' : 'application/json',
            'omitOutputtingOriginalText' : 'true'
        }

        calaisUrl = "https://api.thomsonreuters.com/permid/calais"

        response = requests.post(calaisUrl, headers=headers, data=self._text)

        return response
