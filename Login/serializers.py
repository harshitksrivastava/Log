from rest_framework import serializers
from . models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta():
        model = Profile
        fields = '__all__'
        extra_kwargs ={
            'password':{
                'write_only':True
            }
        }

    def create(self,validated_data):
        return Profile.objects.create_user(**validated_data)

    def updated(self,instance,validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.name= validated_data.get('name',instance.name)
        instance.email = validated_data.get('email',instance.email)
        instance.save()
        return instance
