from rest_framework import serializers
from . models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta():
        model = Profile
        fields = '__all__'

    def create(self,validated_data):
        return Profile.objects.create_user(**validated_data)

    def update(self,validated_data):
        
