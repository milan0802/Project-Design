from django.shortcuts import render,redirect
from .models import User,Product,Wishlist
import requests
import random
# Create your views here.
def index(request):
	return render(request,'index.html')

def seller_index(request):
	return render(request,'seller-index.html')

def category(request):
	products=Product.objects.all()
	return render(request,'category.html',{'products':products})

def single_product(request):
	return render(request,'single-product.html')

def checkout(request):
	return render(request,'checkout.html')

def cart(request):
	return render(request,'cart.html')

def blog(request):
	return render(request,'blog.html')

def single_blog(request):
	return render(request,'single-blog.html')

def tracking(request):
	return render(request,'tracking.html')

def elements(request):
	return render(request,'elements.html')

def contact(request):
	return render(request,'contact.html')

def signup(request):
    if request.method=="POST":
        try:
        	user=User.objects.get(email=request.POST['email'])
        	msg="Email Already Registerd"
        	return render(request,'signup.html',{'msg':msg})
        except:
        	if request.POST['password']==request.POST['cpassword']:
        		User.objects.create(
                        fname=request.POST['fname'],
                        lname=request.POST['lname'],
                        email=request.POST['email'],
                        mobile=request.POST['mobile'],
                        address=request.POST['address'],
                        password=request.POST['password'],
                        profile_picture=request.FILES['profile_picture'],
                        usertype=request.POST['usertype']        
        			)
        		msg="User Registerd Successfuly"
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
				request.session['profile_picture']=user.profile_picture.url
				if user.usertype=="Buyer":
					return render(request,'index.html')
				else:
				    return render(request,'seller-index.html')
			else:
				msg="Incorrect Password"
				return render(request,'login.html',{'msg':msg})
		except:
			msg="Email Not Registerd"
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['profile_picture']
		msg="User Logged Out Successfuly"
		return render(request,'login.html',{'msg':msg})
	except:
		msg="User Logged Out Successfuly"
		return render(request,'login.html',{'msg':msg})

def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		try:
			user.profile_picture=request.FILES['profile_picture']
		except:
			pass
		user.save()
		msg="profile Updated Successfuly"
		if user.usertype=="Buyer":
			return render(request,'profile.html',{'user':user,'msg':msg})
		else:
		    return render(request,'seller-profile.html',{'user':user,'msg':msg})
	else:
		if user.usertype=="Buyer":
			return render(request,'profile.html',{'user':user})
		else:
		    return render(request,'seller-profile.html',{'user':user})

def change_password(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				if user.password!=request.POST['new_password']:
					user.password=request.POST['new_password']
					user.save()
					msg="Password Change Successfuly.Please Login Again."
					del request.session['email']
					del request.session['fname']
					del request.session['profile_picture']
					return render(request,'login.html',{'msg':msg}) 
				else:
					msg="Your New Password can't Be From Your Old Password"
					if user.usertype=="Buyer":
						return render(request,'change-password.html',{'msg':msg})
					else:
					    return render(request,'seller-change-password.html',{'msg':msg})
			else:
				msg="Your New Password & Confirm New Password Dose Not Matched"
				if user.usertype=="Buyer":
					return render(request,'change-password.html',{'msg':msg})
				else:
				    return render(request,'seller-change-password.html',{'msg':msg})
		else:
			msg="Old Password Dose Not Matched"
			if user.usertype=="Buyer":
				return render(request,'change-password.html',{'msg':msg})
			else:
				return render(request,'seller-change-password.html',{'msg':msg})
	else:
		if user.usertype=="Buyer":
			return render(request,'change-password.html')
		else:
		    return render(request,'seller-change-password.html')

def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(mobile=request.POST['mobile'])
			otp=str(random.randint(1000,9999))
			mobile=str(request.POST['mobile'])
			url = "https://www.fast2sms.com/dev/bulkV2"
			querystring = {"authorization":"AnmKGH2R6yRAkDZvOUrMaDZbKqJZihiv7q7dEBQUbu8uvGpAoZFqW8Qz6GRF","variables_values":otp,"route":"otp","numbers":mobile}
			headers = {'cache-control': "no-cache"}
			response = requests.request("GET", url, headers=headers, params=querystring)
			print(response.text)
			request.session['otp']=otp
			request.session['mobile']=mobile
			msg="OTP Send Successfuly"
			return render(request,'otp.html',{'msg':msg})
		except:
			msg="Mobile Not Registerd"
			return render(request,'forgot-password.html',{'msg':msg})
	else:
	    return render(request,'forgot-password.html')

def verify_otp(request):
	otp1=int(request.session['otp'])
	otp2=int(request.POST['otp'])

	if otp1==otp2:
		msg="Set Your New Password"
		del request.session['otp']
		return render(request,'new-password.html',{'msg':msg})
	else:
		msg="Invalid OTP"
		return render(request,'otp.html',{'msg':msg})

def new_password(request):
	if request.POST['new_password']==request.POST['cnew_password']:
		user=User.objects.get(mobile=request.session['mobile'])
		user.password=request.POST['new_password']
		user.save()
		del request.session['mobile']
		msg="Password Updated Successfuly."
		return render(request,'login.html',{'msg':msg})
	else:
		msg="New Password & Confirm New Password Dose Not Matched"
		return render(request,'new-password.html',{'msg':msg})

def seller_add_product(request):
	seller=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		Product.objects.create(
			seller=seller,
			product_catagory=request.POST['product_catagory'],
			product_size=request.POST['product_size'],
			product_name=request.POST['product_name'],
			product_price=request.POST['product_price'],
			product_desc=request.POST['product_desc'],
			product_picture=request.FILES['product_picture'],
		)
		msg="Product Added Successfuly"
		return render (request,'seller-add-product.html',{'msg':msg})
	else:
		return render (request,'seller-add-product.html')

def seller_view_product(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller)
	return render(request,'seller_view_product.html',{'products':products})

def seller_product_details(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,'seller-product-details.html',{'product':product})

def seller_product_edit(request,pk):
	product=Product.objects.get(pk=pk)
	if request.method=="POST":
		product.product_catagory=request.POST['product_catagory']
		product.product_size=request.POST['product_size']
		product.product_name=request.POST['product_name']
		product.product_price=request.POST['product_price']
		product.product_desc=request.POST['product_desc']
		try:
			product.product_picture=request.FILES['product_picture']
		except:
			pass
		product.save()
		msg="Product Updated Successfuly"
		return render(request,'seller-product-edit.html',{'product':product,'msg':msg})
	else:
	    return render(request,'seller-product-edit.html',{'product':product})

def seller_product_delete(request,pk):
	print("Delete")
	product=Product.objects.get(pk=pk)
	product.delete()
	return redirect('seller-view-product')

def product_by_category(request,cat):
	products=[]
	if cat=="all":
		products=Product.objects.all()
	else:
		products=Product.objects.filter(product_catagory=cat)
	return render(request,'category.html',{'products':products})

def product_details(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,'product-details.html',{'product':product})

def add_to_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Wishlist.objects.create(user=user,product=product)
	return redirect('category')

def wishlist(request):
	user=User.objects.get(email=request.session['email'])
	wishlists=Wishlist.objects.filter(user=user)
	return render(request,'wishlist.html',{'wishlists':wishlists})


