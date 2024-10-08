from django.shortcuts import render
from .models import Contact,User
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import random
# Create your views here.
def index(request):
	return render(request,'index.html')

def contact(request):
	if request.method=="POST":
		Contact.objects.create(
                name=request.POST['name'],
                email=request.POST['email'],
                mobaile=request.POST['mobile'],
                remarks=request.POST['remarks']
			)
		msg="Contact Saved Successfuly"
		contacts=Contact.objects.all().order_by("-id")[:3]
		return render(request,'contact.html',{'msg':msg,'contacts':contacts})
	else:
		contacts=Contact.objects.all().order_by("-id")[:3]
		return render(request,'contact.html',{'contact':contacts})

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email Already Registered"
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					mobaile=request.POST['mobaile'],
					address=request.POST['address'],
					password=request.POST['password'],
					profile_picture=request.FILES['profile_picture']
					)
				msg="User Sign UP Successfuly"
				return render(request,'signup.html',{'msg':msg})
			else:
				msg="Password & Confirm Password Dose Not Matched"
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				request.session['email']=user.email
				request.session['fname']=user.fname
				return render(request,'index.html')
			else:
				msg="Incorrect Password"
				return render(request,'login.html',{'msg':msg})
		except:
			msg="Email Not Registered"
			return render(request,'login.html',{'msg':msg})
	else:
	    return render(request,'login.html',)

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		msg="User Logged Out Successfuly"
		return render(request,'login.html',{'msg':msg})
	except:
		msg="User Logged Out Successfuly"
		return render(request,'login.html',{'msg':msg})

def change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				if user.password!=request.POST['new_password']:
					user.password=request.POST['new_password']
					user.save()
					del request.session['email']
					del request.session['fname']
					msg="User Logged Out Successfuly.Please Login Again"
					return render(request,'login.html',{'msg':msg})
				else:
					msg="You New Password Can't be From Your Old Password"
					return render(request,'change-password.html',{'msg':msg})
			else:
				msg="New Password & Confirm New Password Dose Not Matched"
				return render(request,'change-password.html',{'msg':msg})
		else:
			msg="Old Password Dose Not Matched"
			return render(request,'change-password.html',{'msg':msg})
	else:
	    return render(request,'change-password.html')

def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			otp=random.randint(1000,9999)
			subject="OTP For Forgot Password"
			message="Hello "+user.fname+", Your OTP For Forgot Password Is "+str(otp)
			to=[user.email,]
			send_mail(subject, message, settings.EMAIL_HOST_USER, to)
			request.session['email']=user.email
			request.session['otp']=otp
			msg="OTP Send Successfuly"
			return render(request,'otp.html',{'msg':msg})
		except:
			msg="Email Not Registered"
			return render(request,'forgot_password.html',{'msg':msg})
	else:
	    return render(request,'forgot_password.html')

def verify_otp(request):
	otp1=int(request.POST['otp'])
	otp2=int(request.session['otp'])

	if otp1==otp2:
		del request.session['otp']
		return render(request,'new-password.html')
	else:
		msg="Invalid OTP"
		return render(request,'otp.html',{'msg':msg})

def new_password(request):
	if request.POST['new_password']==request.POST['cnew_password']:
		user=User.objects.get(email=request.session['email'])
		user.password=request.POST['new_password']
		user.save()
		msg="Password Updated Successfuly"
		del request.session['email']
		return render(request,'login.html',{'msg':msg})
	else:
		msg="New Password & Confirm Password New Password Dose Not Matched"
		return render(request,'new-password.html',{'msg':msg}) 