from django.urls import path
from . import views



urlpatterns = [ 
    path('', views.StudentView.as_view(), name="StudentView"),
    path('StudentDetailsAPIView/<int:pk>/', views.StudentDetailsAPIView.as_view(), name='StudentDetailsAPIView'),
    path('register/', views.Registration.as_view(), name='register'),
    path('email_verify/', views.VerifyEmail.as_view, name='email_verify')
]