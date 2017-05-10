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
    date_submitted = models.DateTimeField(default=None, null=True)
    simhash = models.CharField(default=None, max_length=500, null=True)

    def __str__(self):
        return "{} of {} ({})".format(self.submission_type,
                                      self.filer,
                                      self.proceeding)

class Person(models.Model):
    full_name = models.CharField(max_length=1000)

    def __str__(self):
        return self.full_name

class Mention(models.Model):
    person = models.ForeignKey(Person)
    filing = models.ForeignKey(Filing)

    def __str__(self):
        return "{} in {}".format(self.person.full_name, self.filing.proceeding)
