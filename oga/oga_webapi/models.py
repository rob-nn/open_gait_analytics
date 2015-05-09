from django.db import models

# Create your models here.

class Patient(models.Model):
    name = models.CharField(max_length=255)
    birth = models.DateTimeField()

class GaitSample(models.Model):
    description = models.CharField(max_length=50)
    date = models.DateTimeField()
    patient = models.ForeignKey(Patient, related_name='samples')
    file_name = models.FileField()
    

class GaitCycle(models.Model):
    descripton = models.CharField(max_length=50)
    initial_contact_frame = models.PositiveIntegerField()
    end_terminal_swing_frame = models.PositiveIntegerField()
    gait_sample = models.ForeignKey('GaitSample')
