from django.db import models
from django.contrib.auth.models import User

class metainformation(models.Model):

    USERID              = models.CharField(max_length=50, blank=False)
    Applicant_name      = models.CharField(max_length=50, blank=False)
    Deceased_name       = models.CharField(max_length=50, blank=False)
    Gender              = models.CharField(max_length=50, blank=False)
    Contact_number      = models.CharField(max_length=10, blank=False)
    Address             = models.CharField(max_length=255, blank=False)
    Deceased_address    = models.CharField(max_length=255, blank=False)
    Date                = models.DateField()
    Date_of_death       = models.DateField()
    time_of_death       = models.TimeField()
    Cause_of_death      = models.CharField(max_length=255, blank=False)
    Relationship        = models.CharField(max_length=50, blank=False)
    Form_number         = models.IntegerField()
    Amount              = models.IntegerField()

    def __str__(self):
        return self.Applicant_name

    class Meta :
        db_table = 'Person_Information'

class contactdetails(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()
    phoneno = models.CharField(max_length=12)
    msg = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta :
        db_table = 'Contact_Us'
