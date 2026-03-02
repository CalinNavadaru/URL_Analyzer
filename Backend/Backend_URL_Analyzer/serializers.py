from rest_framework import serializers
from .models import URLCheck

class URLCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLCheck
        fields = '__all__'