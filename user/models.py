from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	mobile1= models.CharField(max_length=12)
	mobile2= models.CharField(max_length=12)
	adn= models.CharField(max_length=12)
	address=models.CharField(max_length=50)
	gender = models.CharField(max_length=10)
	facebook = models.CharField(max_length=100)
	instagram = models.CharField(max_length=100)
	linkedin = models.CharField(max_length=100)
	pic =models.ImageField(upload_to='myprofile',blank=True)
	dated=models.DateTimeField(auto_now_add=True)
class RelationshipStatus(models.Model):
	profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
	status = models.CharField(max_length=20,default="Single")
	dated=models.DateTimeField(auto_now_add=True)
class Friend_Request(models.Model):
	requested_to = models.ForeignKey(Profile,related_name='requested_to', on_delete=models.CASCADE)
	requested_by = models.ForeignKey(Profile,related_name='requested_by', on_delete=models.CASCADE)
	status = models.CharField(max_length=20,default="not accepted")
	dated=models.DateTimeField(auto_now_add=True)
class Accepted(models.Model):
	user1 = models.ForeignKey(Profile,related_name='user1',on_delete=models.CASCADE)
	user2 = models.ForeignKey(Profile,related_name='user2',on_delete=models.CASCADE)
	dated=models.DateTimeField(auto_now_add=True)

class BreakUp(models.Model):
	requested_b = models.ForeignKey(Profile, related_name="requested_b",on_delete=models.CASCADE)
	requested_t = models.ForeignKey(Profile, related_name="requested_t",on_delete=models.CASCADE)
	status = models.CharField(max_length=20,default="breakup request")
	dated=models.DateTimeField(auto_now_add=True)


class NewChatApp(models.Model):
	message_by = models.ForeignKey(Profile, related_name='messageby',on_delete=models.CASCADE)
	couple = models.ForeignKey(Accepted, related_name='pair', on_delete=models.CASCADE)
	message = models.CharField(max_length=10000)
	dated = models.DateTimeField(auto_now_add=True)