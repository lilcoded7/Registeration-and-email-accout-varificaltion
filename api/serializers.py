from rest_framework import serializers 
from .models import Student
from django.contrib.auth.models import User 




class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']





class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'level', 'course']

