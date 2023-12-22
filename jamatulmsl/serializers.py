from rest_framework import serializers

from .models import metainformation


class metainfoserializer(serializers.ModelSerializer):
     class Meta:
          model = metainformation
          fields = '__all__' 