from django.shortcuts import render,redirect
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from app.models import CustomUser
from django.contrib.auth.decorators import login_required
def base(request):
    return render(request,'base.html')

def index(request):
    return render(request,'index.html')

def dologin(request):
    if request.method == 'POST':
        # Use Django's `authenticate` function directly
        user = authenticate(
            request,
            username=request.POST.get('email'),
            password=request.POST.get('password')
        )
        if user is not None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('hod_home')
            elif user_type == '2':
                return redirect('staff_home')
            elif user_type == '3':
                return redirect('student_home')
            else:

                return redirect('dologin')
        else:
            messages.error(request, 'Invalid Email and Password')
            return redirect('dologin')

    return render(request, 'login.html')

def dologout(request):
    logout(request)
    return redirect('dologin')
@login_required(login_url='dologin')
def profile(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {
        'user':user,
    }
    return render(request,'profile.html')
@login_required(login_url='dologin')
def profile_update(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

    try:
        customuser = CustomUser.objects.get(id=request.user.id)
        customuser.profile_pic = profile_pic
        customuser.first_name = first_name
        customuser.last_name = last_name
        customuser.username = username
        if password !=None and password !='':
            customuser.set_password(password)
        if profile_pic != None and profile_pic != '':
            customuser.profile_pic = profile_pic
        customuser.save()
        messages.success(request,'Your profile sucessfully updated')
        return redirect('profile')
    except:
        messages.error(request,'failed to update your profile')
    return render(request,'profile.html')
