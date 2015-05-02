from rest_framework.serializers import ModelSerializer
from oga_webapi import models

class PatientSerializer(ModelSerializer):
	class Meta:
		model = models.Patient
		fields = ('id', 'name', 'birth')
