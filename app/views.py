from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import auth
from app.forms import MessageForm
from app.models import Message
import datetime


def home(request):
    if ('member_id' in request.session):
       cur_user_id = request.session['member_id']
       cur_user_id = int(cur_user_id)
       return render(request, 'base.html', {'cur_user_id': cur_user_id})
    else:
       return render(request, 'base.html')



@login_required(redirect_field_name='/accounts/login')
def userpage(request, user_id):
    if request.method == "POST":
        income_title = request.POST['title']
        income_text = request.POST['text']
        if income_title and income_text:
            message = Message()
            message.author = request.user
            message.date = datetime.datetime.now()
            message.title = income_title
            message.text = income_text
            message.save()

    user_id = int(user_id)
    current_user_id = request.session['member_id']
    current_user = User.objects.get(id=current_user_id)
    page_owner = User.objects.get(id=user_id)
    message = Message.objects.filter(author=page_owner)
    if current_user_id == user_id:
        message = Message.objects.filter(author=current_user)
        mesform = MessageForm()
        return render(request, 'userpage.html', {'mesform': mesform, 'message': message, 'page_owner': page_owner, 'cur_user_id': current_user_id}, )
    else:
        return render(request, 'user.html', {'message': message, 'page_owner': page_owner, 'cur_user_id': current_user_id}, )


def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    #u = User.objects.get(username=request.POST['username'])
    if user is not None and user.is_active:
        auth.login(request, user)
        request.session['member_id'] = user.id
        return HttpResponseRedirect("/")
    else:
        return render(request, 'login.html')


def register(request):
    cur_user_id = request.session['member_id']
    cur_user_id = int(cur_user_id)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form, 'cur_user_id': cur_user_id})


def logout(request):
    auth.logout(request)
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponseRedirect("/")