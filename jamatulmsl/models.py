from functools import partial
import os
from django.db import models
from django.contrib.auth.models import User


def aadharcard(instance, Aadhar_card, thumbnail=False):
    name, ext = os.path.splitext(Aadhar_card)
    path = f'Aadhar_card/{instance.Contact_number}/{name if thumbnail else ""}{ext}'
    n = 1
    while os.path.exists(path):
        path = f'{instance.Contact_number}/-{n}{ext}'
        n += 1
    return path

def deathcertificate(instance, Death_certificate, thumbnail=False):
    name, ext = os.path.splitext(Death_certificate)
    path = f'Death_certificate/{instance.Contact_number}/{name if thumbnail else ""}{ext}'
    n = 1
    while os.path.exists(path):
        path = f'{instance.Contact_number}/-{n}{ext}'
        n += 1
    return path

def otherfile(instance, Other_file, thumbnail=False):
    name, ext = os.path.splitext(Other_file)
    path = f'Other_file/{instance.Contact_number}/{name if thumbnail else ""}{ext}'
    n = 1
    while os.path.exists(path):
        path = f'{instance.Contact_number}/-{n}{ext}'
        n += 1
    return path

class metainformation(models.Model):

    USERID              = models.CharField(max_length=50, blank=False)
    Applicant_name      = models.CharField(max_length=50, blank=False)
    Deceased_name       = models.CharField(max_length=50, blank=False)
    Deceased_age        = models.CharField(max_length=3, null=True)
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
    Aadhar_card         = models.FileField(upload_to =partial(aadharcard, thumbnail=True), blank=True, null=True, help_text="Browse a photo")
    Death_certificate   = models.FileField(upload_to =partial(deathcertificate, thumbnail=True), blank=True, null=True, help_text="Browse a photo")
    Other_file          = models.FileField(upload_to =partial(otherfile, thumbnail=True), blank=True, null=True, help_text="Browse a photo")

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
