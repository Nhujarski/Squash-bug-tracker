from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index),
    path('register', views.register), #processes registration
    path('login', views.login),#processes login.
    path('dashboard', views.dashboard),#takes us to the dashboard
    path('logout', views.logout), #logs user out
]