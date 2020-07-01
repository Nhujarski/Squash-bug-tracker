from __future__ import unicode_literals
from django.db import models
import re
import bcrypt 

# User validations upon registration.
class UserManager(models.Manager):
    def register_validator(self, post_data):
        user_errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PW_REGEX = re.compile(r'^(?=.{8,}$)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?\W).*$')
        if not PW_REGEX.match(post_data['password']):
            user_errors["weak_pw"]="Password must be at least 8 characters long must contain at least: 1 uppercase letter,1 lowercase letter,1 number and 1 special character"
        if post_data["password"]!=post_data["confirm_pw"]:
            user_errors["confirm_pw"] = "Password did not match confirmation"
        if len(post_data['first_name']) < 2:
            user_errors['first_name'] = 'Please enter a longer first name'
        if len(post_data['last_name']) < 2:
            user_errors['last_name'] = 'Please enter a longer last name'
        all_user = User.objects.filter(email=post_data['email'])
        if len(all_user)>0:
            user_errors['duplicate_email'] = 'That email is already in use. Please choose another one'
        
        if not EMAIL_REGEX.match(post_data['email']):
            user_errors['email'] = "Invalid email address!"
        if len(post_data['password'])<6:
            user_errors['password'] = 'Please enter a longer password'
        if post_data['password']!=post_data['confirm_pw']:
            user_errors['confirm'] = 'Your passwords do not match. Try again'

        return user_errors

# login errors and validations upon login
    def login_validator(self, post_data):
        login_errors={}
        current_user_list = User.objects.filter(email=post_data['email'])
        if len(current_user_list) < 1:
            login_errors['email'] = 'This email does not exist. Please register instead'
        elif not bcrypt.checkpw(post_data['password'].encode(), current_user_list[0].password.encode()):
            login_errors['password'] = 'Incorrect password. Try again'
        return login_errors
        
# the actual user class to create
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    objects = UserManager()

# class used for validtions of project class
class ProjectManager(models.Manager):
    def project_validator(self, post_data):
        project_errors = {}

        if len(post_data['project_name']) < 3:
            project_errors['project_name'] = 'Project names must be longer than 3 characters. Please try again.'
        return project_errors

# actual class that creates a specific project
class Project(models.Model):
    project_name = models.CharField(max_length=255)
    project_desc = models.TextField()
    user = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProjectManager()

# class used for validations of bug class
class BugManager(models.Manager):
    def bug_validator(self, post_data):
        bug_errors = {}

        if len(post_data['bug_name']) < 2:
            bug_errors['bug_name'] = 'Name must be onger than  2 characters. Please enter a valid name.'
        if len(post_data['desc']) < 2:
            bug_errors['desc'] = 'Descritption must be loger than 2 characters. Please enter a valid Description.'
        return bug_errors


# actual class that creates bugs
class Bug(models.Model):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    Priority_Choices = (
    ('LOW', 'Low'),
    ('MEDIUM', 'Medium'),
    ('HIGH','High',),
    )
    bug_name = models.CharField(max_length=255)
    desc = models.TextField()
    priority = models.CharField(max_length=10, choices=Priority_Choices, default=LOW)
    project = models.ForeignKey(Project, related_name='bugs', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BugManager()