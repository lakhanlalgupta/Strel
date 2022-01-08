from django.shortcuts import render
from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import Profile, RelationshipStatus, Accepted, NewChatApp
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def user(request):
	return render(request,'user.html')

@login_required(login_url='/login')
def chat(request):
	user = Profile.objects.get(user__username=request.user)
	relationship = RelationshipStatus.objects.get(profile=user)
	if relationship.status == "Single" or relationship.status == "Trying":
		return redirect('/login')

	user = Profile.objects.get(user__username=request.user)

	pair = Accepted.objects.filter(user1=user)
	user2={}
	if pair:
		for i in pair:
			user2 = i.user2
	else:
		pair = Accepted.objects.filter(user2=user)
		for i in pair:
			user2 = i.user1
	for i in pair:
		pair = i
		break
	print(user)
	msg = request.GET.get('msg')
	if msg:
		chat = NewChatApp(couple= pair,message_by=user, message=msg)
		chat.save()
		return redirect('/chat')
	
	chatdata = NewChatApp.objects.filter(couple=pair).order_by('-dated')
	
	return render(request,'newchat.html',{'chatdata':chatdata,'user2':user2,'user':user})

@login_required(login_url='/login')
def deactivate(request):
	user = Profile.objects.get(user__username=request.user)
	relationship = RelationshipStatus.objects.get(profile=user)
	if relationship.status == "In Open Relationship":
		return redirect('/welcome')
	user = User.objects.filter(username=user.user.username)
	user.delete()

	return redirect('/registration')

@login_required(login_url='/login')
def welcome(request):
	user = Profile.objects.get(user__username=request.user)
	relationship = RelationshipStatus.objects.get(profile=user)
	if relationship.status == "Single" or relationship.status == "Trying":
		return redirect('/login')
	pair = Accepted.objects.filter(user1=user)
	user2={}
	if pair:
		for i in pair:
			user2 = i.user2
	else:
		pair = Accepted.objects.filter(user2=user)
		for i in pair:
			user2 = i.user1


	return render(request,'welcome.html',{'fulldata':user2,'user':user})


def registration(request):
	if request.method=='POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		mobile1 = request.POST['mobile1']
		mobile2 = request.POST['mobile2']
		address = request.POST['address']
		adn = request.POST['adn']
		gender = request.POST['gender']
		if gender == 'not_selected':
			message = "Please Choose Your Gender Also..."
			messages.info(request, message)
			return redirect('/registration')
		dimage = request.FILES['pic1']
		facebook = request.POST['facebook']
		instagram = request.POST['instagram']
		linkedin = request.POST['linkedin']

		if 'www' in facebook:
			facebook = facebook.split('/')
			facebook = facebook[-2]
		else:
			facebook = facebook
		if 'www' in instagram:
			instagram = instagram.split('/')
			instagram = instagram[-2]
		else:
			instagram = instagram
		if 'www' in linkedin:
			linkedin = linkedin.split('/')
			linkedin = linkedin[-2]
		else:
			linkedin = linkedin
		password = request.POST['password']
		password_confirmation = request.POST['password_confirmation']

		u=User(first_name=first_name,last_name=last_name,email=email,username=email,password=make_password(password_confirmation))
		u.save()
		p=Profile(user=u,mobile1=mobile1,mobile2=mobile2,gender=gender,adn=adn,address=address,pic=dimage,facebook=facebook,instagram=instagram,linkedin=linkedin)
		p.save()
		r=RelationshipStatus(profile=p)
		r.save()
		return redirect('/login')

		print(first_name,last_name,email,mobile1,mobile1,address,adn,gender,dimage,password,password_confirmation)
	return render(request,'registration.html')

def login_call(request):
	if request.method=="POST":
		email_address = request.POST['email_address']
		password = request.POST['password']
		currentUser=authenticate(username=email_address,password=password)
		if currentUser:
			login(request,currentUser)
			u=Profile.objects.get(user__username=request.user)
			relationship = RelationshipStatus.objects.get(profile=u)
			if relationship.status == "In Open Relationship":
				return redirect('/welcome')
			elif relationship.status=="Protected":
				return redirect('/waiting')
			else:
				if u.gender=='male':
					print("Male")
					return redirect('/maleapp')
				if u.gender=='female':
					print("Female")
					return redirect('/femaleapp')
				
		else:
			return redirect('/login')
	return render(request,'login.html')
def logout_call(request):
	logout(request)
	return redirect('/')