from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Myuser
# Create your views here.
def usignup(request):
    if request.method =='POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name'] 
        password = request.POST['password'] 
        confirm_password =request.POST['confirm_password']
        if Myuser.objects.filter(email=email).exists():
            return render(request,'signup.html',{'error':'Email already exists'}) 
        if password !=confirm_password:
            return render(request,'signup.html',{'error':'Passwords do not match'})
        my_user =Myuser.objects.create(email=email,first_name=first_name,last_name=last_name,password=password)
        my_user.save() 
        print("signup Successful")
        messages.success(request,'Account has been created successfully')
        return redirect('login')
    return render(request, 'signup.html')
  
def ulogin(request):
    if request.method == 'POST':   
        email =request.POST['email']
        password =request.POST['password']
        try:
            user = Myuser.objects.get(email=email, password=password)
            if user is not None:
                session = request.session
                session['user_id'] = user.u_id
                session['first_name'] = user.first_name
                print("Login Successful")   
                return redirect('dashboard')
        except Myuser.DoesNotExist:
            print('login failed')
            messages.warning(request,'Invalid credentials')
            return redirect('login')
     
    return render(request,'login.html')
