from django.shortcuts import render
from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from user.models import Profile, RelationshipStatus, Friend_Request, Accepted, BreakUp
from django.contrib.auth.models import User
from django.contrib import messages

@login_required(login_url='/login')
def home(request):
	gender = "female"

	check = Profile.objects.get(user__username=request.user)
	relationship = RelationshipStatus.objects.get(profile=check)
	if relationship.status == "In Open Relationship":
		return redirect('/welcome') 

	currentUser = check.user.username
	db = Profile.objects.filter(gender='female')
	for i in db:
		if i.user.username ==currentUser:
			return redirect('/login')
		else:
			pass

	myprofile = Profile.objects.get(user__username=request.user)

	data = Profile.objects.filter(gender=gender)
	return render(request,'maleapp.html',{'maledata':data,'myprofile':myprofile})
@login_required(login_url='/login')
def fullprofile(request,id):
	u=Profile.objects.get(user__username=request.user)
	relationship = RelationshipStatus.objects.get(profile=u)

	db = Profile.objects.get(id=id)
	if db.gender =='male':
		return redirect('/login')
	elif relationship.status == "In Open Relationship":
		return redirect('/welcome')
	else:
		fulldata = Profile.objects.get(id=id)
		myprofile = Profile.objects.get(user__username=request.user)
		relationship = RelationshipStatus.objects.get(profile=id)
		return render(request,'fullprofileofgirl.html',{'fulldata':fulldata,'myprofile':myprofile,'relationship':relationship})


@login_required(login_url='/login')
def NextProcess(request,id):
	user = Profile.objects.get(user__username=request.user)

	relationship = RelationshipStatus.objects.get(profile=user)
	if relationship.status == "In Open Relationship":
		return redirect('/welcome')
	if relationship.status == "Protected":
		return redirect('/waiting')

	requested_to = Profile.objects.get(id=id)
	relationship = Accepted.objects.all()
	inopen = []
	for i in relationship:
		inopen.append(i.user1.user.username)
		inopen.append(i.user2.user.username)
	print(inopen)
	if requested_to.gender =='male':
		return redirect('/login')
	elif requested_to.user.username in inopen:
		return redirect('/login')
	else:
		f_q = Friend_Request(requested_by = user, requested_to = requested_to)
		f_q.save()
		RelationshipStatus.objects.filter(profile=user).update(status="Trying")
		return redirect('/maleapp')


@login_required(login_url='/login')
def rrtomale(request):
	user = Profile.objects.get(user__username=request.user)
	relationship = RelationshipStatus.objects.get(profile=user)
	if relationship.status == "In Open Relationship":
		return redirect('/welcome')

	f_q = Friend_Request.objects.filter(requested_to=user)
	return render(request,'rrtomale.html',{'f_q':f_q})

@login_required(login_url='/login')
def rejectthisgirl(request,id):
	user = Profile.objects.get(user__username=request.user)
	relationship = RelationshipStatus.objects.get(profile=user)
	if relationship.status == "In Open Relationship":
		return redirect('/welcome')

	f_q = Friend_Request.objects.get(id=id)
	f_q.delete()
	return redirect('/maleapp/rrtomale')

@login_required(login_url='/login')
def acceptthisgirl(request,id):
	user = Profile.objects.get(user__username=request.user)
	relationship = RelationshipStatus.objects.get(profile=user)
	if relationship.status == "In Open Relationship":
		return redirect('/welcome')
	db = Profile.objects.get(id=id)
	if db.gender =='male':
		return redirect('/login')
	else:
		user1 = Profile.objects.get(user__username=request.user)
		user2 = Profile.objects.get(id=id)
		pair = Accepted(user1=user1,user2=user2)
		pair.save()
		RelationshipStatus.objects.filter(profile=user1).update(status="In Open Relationship")
		RelationshipStatus.objects.filter(profile=user2).update(status="In Open Relationship")
		f_q = Friend_Request.objects.filter(requested_to=user1)
		f_q.delete()
		f_q = Friend_Request.objects.filter(requested_by=user1)
		f_q.delete()
		f_q = Friend_Request.objects.filter(requested_to=user2)
		f_q.delete()
		f_q = Friend_Request.objects.filter(requested_by=user2)
		f_q.delete()
		print("Accepted")
		return redirect('/welcome')

def brtofemale(request,id):
	user = Profile.objects.get(user__username=request.user)
	relationship = RelationshipStatus.objects.get(profile=user)
	if relationship.status == "Single" or relationship.status == "Trying":
		return redirect('/login')

	db = Profile.objects.get(id=id)
	relationship = RelationshipStatus.objects.get(profile=db)
	if db.gender =='male':
		return redirect('/login')
	elif relationship.status == "Single" or relationship.status == "Trying":
		return redirect('/login')
	else:
		requested_by = Profile.objects.get(user__username=request.user)
		requested_to = Profile.objects.get(id=id)
		b_q = BreakUp(requested_b = requested_by, requested_t=requested_to)
		b_q.save()
		message = "Break-up request sent successfully..."
		messages.info(request, message)
		return redirect('/welcome')

def brtomalelist(request):
	user = Profile.objects.get(user__username=request.user)
	relationship = RelationshipStatus.objects.get(profile=user)
	if relationship.status == "Single" or relationship.status == "Trying":
		return redirect('/login')

	user = Profile.objects.get(user__username=request.user)
	b_q = BreakUp.objects.filter(requested_t = user)
	return render(request,'brtomalelist.html',{'b_q':b_q})

def brdeclinebymale(request):
	user = Profile.objects.get(user__username=request.user)
	relationship = RelationshipStatus.objects.get(profile=user)
	if relationship.status == "Single" or relationship.status == "Trying":
		return redirect('/login')

	user = Profile.objects.get(user__username=request.user)
	b_q = BreakUp.objects.filter(requested_t = user)
	b_q.delete()
	b_q = BreakUp.objects.filter(requested_b = user)
	b_q.delete()
	return redirect('/welcome')


def yesBreakUp(request):
	user = Profile.objects.get(user__username=request.user)
	relationship = RelationshipStatus.objects.get(profile=user)
	if relationship.status == "Single" or relationship.status == "Trying":
		return redirect('/login')
		
	user = Profile.objects.get(user__username=request.user)
	b_q = BreakUp.objects.filter(requested_t = user)
	for i in b_q:
		RelationshipStatus.objects.filter(profile=i.requested_t).update(status="Single")
		RelationshipStatus.objects.filter(profile=i.requested_b).update(status="Single")
	b_q.delete()
	b_q = BreakUp.objects.filter(requested_b = user)
	for i in b_q:
		RelationshipStatus.objects.filter(profile=i.requested_t).update(status="Single")
		RelationshipStatus.objects.filter(profile=i.requested_b).update(status="Single")
	b_q.delete()
	Accepted_data = Accepted.objects.filter(user1=user)
	Accepted_data.delete()
	Accepted_data = Accepted.objects.filter(user2=user)
	Accepted_data.delete()

	return redirect('/maleapp')

def superbreakup(request):
	user = Profile.objects.get(user__username=request.user)
	relationship = RelationshipStatus.objects.get(profile=user)
	if relationship.status == "Single" or relationship.status == "Trying":
		return redirect('/login')

	user = Profile.objects.get(user__username=request.user)
	b_q = BreakUp.objects.filter(requested_b = user)
	if b_q:
		b_q = BreakUp.objects.filter(requested_t = user)

		for i in b_q:
			RelationshipStatus.objects.filter(profile=i.requested_t).update(status="Single")
			RelationshipStatus.objects.filter(profile=i.requested_b).update(status="Single")
		b_q.delete()
		b_q = BreakUp.objects.filter(requested_b = user)
		for i in b_q:
			RelationshipStatus.objects.filter(profile=i.requested_t).update(status="Single")
			RelationshipStatus.objects.filter(profile=i.requested_b).update(status="Single")
		b_q.delete()
	else:
		message = "First Try Normal Break-Up..."
		messages.info(request, message)
		return redirect('/welcome')

	Accepted_data = Accepted.objects.filter(user1=user)
	Accepted_data.delete()
	Accepted_data = Accepted.objects.filter(user2=user)
	Accepted_data.delete()
	return redirect('/maleapp')