from rest_framework import viewsets
from rest_framework import permissions
from oga_webapi import serializers
from oga_webapi import models


class PatientViewSet(viewsets.ModelViewSet):
	queryset = models.Patient.objects.all()
	serializer_class = serializers.PatientSerializer
        permission_classes = [
                permissions.AllowAny
	]
