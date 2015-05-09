from rest_framework.serializers import ModelSerializer
from oga_webapi import models
import rest_framework.serializers as serializers


class GaitSampleSerializer(ModelSerializer):
	class Meta:
		model = models.GaitSample
		fields = ('id', 'description', 'date', 'patient')

class PatientSerializer(ModelSerializer):
	samples = GaitSampleSerializer(many=True, read_only=True);
	class Meta:
		model = models.Patient
		fields = ('id', 'name', 'birth', 'samples')


