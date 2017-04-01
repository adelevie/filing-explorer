from django.db import models

from django.contrib.postgres.fields import ArrayField

class Filing(models.Model):
    proceeding = models.CharField(max_length=200)
    proceedings = ArrayField(models.CharField(max_length=200))
    text = models.TextField(null=True)
    fcc_id = models.CharField(max_length=200)
    contact_email = models.CharField(max_length=200, null=True)
    submission_type = models.CharField(max_length=200, null=True)
    filer = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=200, null=True)
    documents = ArrayField(models.CharField(max_length=1000))

    def __str__(self):
        return "{} of {} ({})".format(self.submission_type.lower().capitalize(),
                                      self.filer,
                                      self.proceeding)
