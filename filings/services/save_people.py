from filings.models import Filing, Person, Mention

from filings.services.get_open_calais_entities import GetOpenCalaisEntities, CalaisError
from filings.services.open_calais_parser import OpenCalaisParser

from IPython import embed

import time

class SavePeople(object):
    def __init__(self, api_key, proceeding):
        self._api_key = api_key
        self._proceeding = proceeding

    def perform(self):
        mentions = Mention.objects.all()

        filings_ids_that_have_mentions = []
        for mention in mentions:
            filings_ids_that_have_mentions.append(mention.filing.pk)

        # filter out filings that already have mentions associated with them
        # this way, we only pick up where we left off
        filings = Filing.objects \
                    .filter(proceeding=self._proceeding) \
                    .exclude(pk__in=filings_ids_that_have_mentions)

        for filing in filings:
            if filing.text is not None:
                try:
                    time.sleep(1)
                    get_open_calais_entities = GetOpenCalaisEntities(self._api_key,
                                                                     filing.text)

                    entities_response = get_open_calais_entities.perform()
                    entities = entities_response.json()

                    calais_parser = OpenCalaisParser(entities)

                    names = calais_parser.names()

                    for name in names:
                        person, created = Person.objects.get_or_create(
                            full_name=name
                        )

                        mention, created = Mention.objects.get_or_create(
                            person=person,
                            filing=filing
                        )
                except CalaisError as err:
                    print(err)
