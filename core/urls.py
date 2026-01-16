from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register, name='register'),
    path('test/', views.test_page, name='test_page'),
    path('api/questions/', views.get_questions, name='get_questions'),
    path('api/submit/', views.submit_test, name='submit_test'),
    path('result/', views.result_page, name='result_page'),
]
