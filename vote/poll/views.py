from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .forms import RegistrationForm,CandidateProForm,ChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Candidate,ControlVote,Position
from django.utils import timezone
from django.urls import reverse
from io import StringIO
import csv

def homeView(request):
    return render(request, "poll/home.html")

def registrationView(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] == cd['confirm_password']:
                obj = form.save(commit=False)
                obj.set_password(obj.password)
                obj.save()
                messages.success(request, 'You have been registered.')
                return redirect('home')
            else:
                return render(request, "poll/registration.html", {'form':form,'note':'password must match'})
    else:
        form = RegistrationForm()

    return render(request, "poll/registration.html", {'form':form})

def loginView(request):
    if request.method == "POST":
        usern = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(request, username=usern, password=passw)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.success(request, 'Invalid username or password!')
            return render(request, "poll/login.html")
    else:
        return render(request, "poll/login.html")


@login_required
def logoutView(request):
    logout(request)
    return redirect('home')

@login_required
def dashboardView(request):
    return render(request, "poll/dashboard.html")

@login_required
def positionView(request):
    obj = Position.objects.filter(end_at__gte = timezone.now(),start_at__lte=timezone.now())
    return render(request, "poll/position.html", {'obj':obj})

@login_required
def candidateView(request, pos):
    obj = get_object_or_404(Position, pk = pos)
    if request.method == "POST":

        temp = ControlVote.objects.get_or_create(user=request.user, position=obj)[0]

        if temp.status == False:
            temp2 = Candidate.objects.get(pk=request.POST.get(obj.title))
            temp2.total_vote += 1
            temp2.save()
            temp.status = True
            temp.save()
            return HttpResponseRedirect('/position/')
        else:
            messages.success(request, 'you have already been voted this position.')
            return render(request, 'poll/candidate.html', {'obj':obj})
    else:
        return render(request, 'poll/candidate.html', {'obj':obj})

@login_required
def resultView(request):
    obj = Candidate.objects.all().order_by('position','-total_vote')
    return render(request, "poll/result.html", {'obj':obj})

@login_required
def candidateDetailView(request, id):
    obj = get_object_or_404(Candidate, pk=id)
    return render(request, "poll/candidate_detail.html", {'obj':obj})


@login_required
def changePasswordView(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "poll/password.html", {'form':form})


@login_required
def editProfileView(request):
    if request.method == "POST":
        form = ChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ChangeForm(instance=request.user)
    return render(request, "poll/edit_profile.html", {'form':form})


def candidateloginView(request):
    if request.method == "POST":
        usern = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(request, username=usern, password=passw)
        if user is not None:
            login(request,user)
            cand = get_object_or_404(Candidate,user = user)
            return HttpResponseRedirect(reverse('candidateprofile',kwargs={'id':cand.id}))
        else:
            messages.success(request, 'Invalid username or password!')
            return HttpResponseRedirect(reverse('candidatelogin'))
    else:
        return render(request, "poll/login.html")
@login_required
def candidateEditView(request,id):
    candid = get_object_or_404(Candidate,id = id)
    if request.method == "POST":
        form = CandidateProForm(request.POST,request.FILES, instance=candid)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('candidateprofile',kwargs={'id':id}))
    else:
        form = CandidateProForm(instance=request.user)
    return render(request, "poll/edit_candidate_profile.html", {'form':form,'id':id})
@login_required   
def candidateProfileView(request, id):
    obj = get_object_or_404(Candidate, pk=id)
    return render(request, "poll/candidate_profile.html", {'obj':obj,'id':id})

def processView(request):
    if(request.method == "POST"):
        form1 = request.FILES['csvfile']
        name = form1.name.split('.')
        if(name[-1] != 'csv'):
            messages.error(request,"file not valid!")
            return HttpResponseRedirect(reverse('home'))
        else:
            upfile = form1.read().decode('utf-8')
            reader = csv.reader(StringIO(upfile))
            created_users = []
            existing_users = []
            for i,line in enumerate(reader):
                if(i==0):
                    pass
                else:
                    line = "".join(line)
                    line = line.split(';')
                    line.pop()
                    user,Created = User.objects.get_or_create(username = line[0])
                    if(Created):
                        user.first_name = line[1]
                        user.last_name = line[2]
                        user.email = line[3]
                        user.is_active = True
                        user.set_password(line[4])
                        user.save()
                        created_users.append(user.username)
                    else:
                        existing_users.append(user.username)
            created_users = ' '.join(created_users)
            existing_users = ' '.join(existing_users)
            messages.success(request,"{} created and {} already exist(s)".format("user(s) " + created_users if created_users else "No user is ",
            "user(s) " + existing_users if existing_users else "0 user "))
            return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, "poll/registration.html")