from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt 

# Create your views here.
def index(request):
    return render(request,'index.htm')

# process the registration of a user.
def register(request):
    form = request.POST
    errors_returned = User.objects.register_validator(form)
    # print(errors_returned)
    if len(errors_returned) > 0:
        request.session['register_error'] = True
        for single_error in errors_returned.values():
            messages.error(request, single_error)
        return redirect('/')
    hashed_pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(first_name=form['first_name'], last_name=form['last_name'], email=form['email'], password=hashed_pw)
    request.session['user_id']=new_user.id
    return redirect('/dashboard')

# process the login of a user.
def login(request):
    form = request.POST
    login_errors = User.objects.login_validator(form)
    if len(login_errors) > 0:
        request.session['register_error'] = False
        for login_error in login_errors.values():
            messages.error(request, login_error)
        return redirect('/')
    user_id = User.objects.get(email=form['email']).id
    request.session['user_id'] = user_id    
    return redirect('/dashboard')

# renders dashboard page
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'projects': Project.objects.all()
    }
    return render(request, 'dashboard.htm', context)

# handles logout
def logout(request):
    request.session.clear()
    return redirect('/')

# renders new project page
def new_project(request):
    context = {
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request,'addproject.htm', context)

# handels adding a new project to data base.
def add_project(request):
    
    form = request.POST
    errors_returned = Project.objects.project_validator(form)
    # print(errors_returned)
    if len(errors_returned) > 0:
        request.session['project_error'] = True
        for single_error in errors_returned.values():
            messages.error(request, single_error)
        return redirect('projects/new')
    if len(errors_returned) == 0:
        current_user = User.objects.get(id=request.session['user_id'])
        new_project = Project.objects.create(project_name=form['project_name'],project_desc=form['project_desc'],user=current_user)
        return redirect('/projects/' + str(Project.objects.last().id))

# show project details page
def project_details(request,id):
    my_project = Project.objects.get(id=id)
    context = {
        'project' : my_project
    }
    return render(request,'projectdetails.htm',context)

# method that renders edit job page.
def project_edit(request,id):
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'project': Project.objects.get(id=id),

    }
    return render(request,'editproject.htm',context)

# method to edit project in database.
def edit(request,id):
    if request.method != 'POST':
        return redirect('/dashboard')

    form = request.POST
    errors_returned = Project.objects.project_validator(form)
    # print(errors_returned)
    if len(errors_returned) > 0:
        request.session['project_error'] = True
        for single_error in errors_returned.values():
            messages.error(request, single_error)
        return redirect(f'/projects/edit/{id}')

    job_to_update = Project.objects.get(id=id)
    job_to_update.project_name = form['project_name']
    job_to_update.project_desc = form['project_desc']
    job_to_update.save()

    return redirect(f'/projects/{id}')

# method to delete specific project from database.
def delete(request, id):
    project_to_delete = Project.objects.get(id=id)
    project_to_delete.delete()
    return redirect('/dashboard')