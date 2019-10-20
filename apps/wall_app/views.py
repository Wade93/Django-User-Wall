from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Message, Comment
from datetime import datetime

def index(request):
    if 'user_id' in request.session:
        return redirect('/wall')
    if 'fname' not in request.session:
        request.session['fname'] = ""
    if 'lname' not in request.session:
        request.session['lname'] = ""
    if 'email' not in request.session:
        request.session['email'] = ""
    return render(request, "wall_app/index.html")

def wall(request):
    if request.session['fname'] == "":
        return redirect('/')
    
    context = {
        "wall_messages" : Message.objects.all(),
        "comments" : Comment.objects.all(),
        "Now" : datetime.now(),
    }

    print(context['Now'])

    return render(request, "wall_app/wall.html", context)

def register_new_user(request):
    request.session['fname'] = request.POST['fname']
    request.session['lname'] = request.POST['lname']
    request.session['email'] = request.POST['email']
    request.session['bdate'] = request.POST['bdate']

    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        User.objects.create(first_name = request.POST['fname'], last_name = request.POST['lname'], email = request.POST['email'], date_of_birth = request.POST['bdate'], password = pw_hash)

        request.session['user_id'] = User.objects.get(email = request.POST['email']).id
        return redirect('/wall')

def login_user(request):
    errors = User.objects.log_in_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/')
    else:
        request.session['user_id'] = User.objects.get(email = request.POST['email']).id
        request.session['fname'] = User.objects.get(email = request.POST['email']).first_name
        return redirect('/wall')

def post_message(request):
    user = User.objects.get(id = request.session['user_id'])
    Message.objects.create(user = user, message = request.POST['message'])
    
    return redirect('/wall')

def delete_message(request):
    message_to_delete = Message.objects.get(id = int(request.POST['message_id']))
    message_to_delete.delete()
    return redirect('/wall')

def post_comment(request):
    user = User.objects.get(id = request.session['user_id'])
    message = Message.objects.get(id = request.POST['message_id'])
    Comment.objects.create(user = user, message = message, comment = request.POST['comment'])

    return redirect('/wall')

def delete_comment(request):
    comment_to_delete = Comment.objects.get(id = int(request.POST['comment_id']))
    comment_to_delete.delete()
    return redirect('/wall')

def clear(request):
    request.session.clear()
    return redirect('/')

def logout_user(request):
    request.session.clear()
    return redirect('/')