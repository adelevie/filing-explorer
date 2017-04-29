from filings.models import Filing

class FilingTemplateModel(object):
    def __init__(self, filing):
        self._filing = filing

    def summary(self):
        summary = ""
        if self._filing.text:
            summary = self._filing.text[:80] + "..."
        return summary

    def heading(self):
        return "{} of {} ({})".format(self._filing.submission_type,
                                      self._filing.filer,
                                      self._filing.proceeding)

    def url_path(self):
        return "/filings/{}/".format(self._filing.id)
