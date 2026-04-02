from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm


# Create your views here.
def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    topic=Topic.objects.all()[0:5]
    room=Room.objects.filter(Q(topic__name__icontains=q)|
                             Q(name__icontains=q)|
                             Q(descripton__icontains=q))
    room_count=room.count()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))[0:5]
    context={'room':room,
              'topics': topic,
              'room_count':room_count,
              'room_messages':room_messages}
    return render(request,"base/home.html",context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages= room.message_set.all().order_by('-created')
    participants=room.participants.all()
    if request.method == 'POST':
        messages=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room-page', pk=room.id)
    context={'room':room,
             'room_messages':room_messages,
             'participants':participants}
    return render(request,"base/rooms.html",context)

@login_required(login_url='/login')
def createRoom(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            descripton=request.POST.get('descripton')
        )
        return redirect('home') 
    context={'form':form,
             'topics':topics}
    return render(request,"base/room_form.html",context)

@login_required(login_url='/login')
def updateRoom(request, pk):
    room=Room.objects.get(id=pk)
    topic=Topic.objects.all()
    form=RoomForm(instance=room)
    if room.host != request.user:
        return HttpResponse('<h1>You are not authorizerd to do this!!!</h1>')
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.descripton=request.POST.get('descripton')
        room.save()
        return redirect('home')
    context={'form':form,
             'topics':topic,
             'room':room}
    return render(request,"base/room_form.html",context)

@login_required(login_url='/login')
def deleteRoom(request, pk):
    room=Room.objects.get(id=pk)
    if room.host != request.user:
        return HttpResponse('You are not authorizerd to do this!!!')
    if request.method=='POST':
        room.delete()
        return redirect('room-page', pk=room.id)
    context={"obj":room}
    return render(request, 'base/delete.html', context)

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist")
        user=authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user=user)
            return redirect('home')
        else:
            messages.error(request, "Username or password is wrong.")
    context={'page':page}
    return render(request, 'base/login_form.html', context)

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occoured during registration!!')
    form=MyUserCreationForm()
    context={'form':form}
    return render(request,'base/login_form.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login')
def deletMessage(request, pk):
    message=Message.objects.get(id=pk)
    if message.user != request.user:
        return HttpResponse('You are not authorizerd to do this!!!')
    if request.method=='POST':
        message.delete()
        return redirect('home')
    context={"obj":message}
    return render(request, 'base/delete.html', context)

def userProfile(request, pk):
    user=User.objects.get(id=pk)
    room=user.room_set.all()
    room_messages=user.message_set.all()[0:5]
    topics=Topic.objects.all()
    context={'user':user,
             'room':room,
             'room_messages':room_messages,
             'topics':topics}
    return render(request,'base/profile.html',context)

@login_required(login_url='/login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method=='POST':
        form=UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context={'form':form}
    return render(request,'base/update_user.html',context=context)

def topicPage(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    topics=Topic.objects.filter(name__icontains=q)
    context={'topics':topics}
    return render(request,'base/topics.html',context=context)

def activityPage(request):
    room_messages=Message.objects.all()
    context={'room_messages':room_messages}
    return render(request,'base/activity.html',context)