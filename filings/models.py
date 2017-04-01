from django.db import models

class Proceeding(models.Model):
    name = models.CharField(max_length=200)
    bureau_name = models.CharField(max_length=200, null=True)
    bureau_code = models.CharField(max_length=200, null=True)
    fcc_id = models.CharField(max_length=200)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

class Filing(models.Model):
    proceeding = models.ForeignKey(Proceeding, on_delete=models.CASCADE)
    text = models.TextField(null=True)
    fcc_id = models.CharField(max_length=200)
    contact_email = models.CharField(max_length=200, null=True)
    submission_type = models.CharField(max_length=200, null=True)
    filer = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=200, null=True)

    def __str__(self):
        return "{} of {} ({})".format(self.submission_type.lower().capitalize(),
                                      self.filer,
                                      self.proceeding.name)
