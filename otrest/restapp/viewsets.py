from rest_framework import viewsets
from . import models
from . import serializers

class InfoViewset(viewsets.ModelViewSet):
    queryset = models.Info.objects.all()
    serializer_class = serializers.InfoSerializer