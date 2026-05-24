from . import views
from django.urls import path

urlpatterns = [
    path('hello', views.say_hello, name='say_hello'),
]
