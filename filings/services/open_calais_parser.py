class OpenCalaisParser(object):
    def __init__(self, calais_entities_response):
        self._calais_entities_response = calais_entities_response

    def names(self):
        people = []
        for key, value in self._calais_entities_response.items():
            if value.get('_type') == 'Person':
                people.append(value.get('name'))
        return people
