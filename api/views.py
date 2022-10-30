from django.shortcuts import render
from rest_framework.views import APIView 
from .serializers import StudentSerializer, RegistrationSerializer
from .models import Student
from rest_framework.response import Response 
from rest_framework import status 
from django.http import Http404
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics
from django.urls import reverse




# Create your views here.


class Registration(APIView):
    # POST REQUEST 
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            
        

    # jwt token generation 
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user).access_token 

            current_site = get_current_site(request).domain
            relativeLink = reverse('email_verify')
            
            absurl = 'http://' + current_site + relativeLink + '?token=' + str(token) 
            email_body = 'Hello ' + user.username + ' click the link below to verify your account \n' + absurl
            data = {
                'email_subject' : 'verify Email',
                'email_body'    : email_body,
                'to_email'      : user.email,
                  
            }  

            Util.send_email(data)
            return Response('kindy check your email accout to verify your account')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(generics.GenericAPIView):
    pass 


class StudentView(APIView):
    def get(self, request):
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()

            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# update class api view 

class StudentDetailsAPIView(APIView):
    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student    = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONDENT)
        