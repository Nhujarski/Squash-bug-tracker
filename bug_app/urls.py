from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index),
    path('register', views.register), #processes registration
    path('login', views.login),#processes login.
    path('dashboard', views.dashboard),#takes us to the dashboard
    path('logout', views.logout), #logs user out
    path('projects/new', views.new_project), #renders add project page
    path('add_project', views.add_project), #adds project to database
    path('projects/<int:id>', views.project_details), # path to view project details.
]