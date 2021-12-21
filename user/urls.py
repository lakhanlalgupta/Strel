from . import views
from django.urls import path, include

app_name='user'

urlpatterns = [
	path('', views.user),
	path('registration', views.registration,name="registration"),
	path('maleapp',include('maleapp.urls', namespace='maleapp')),
	path('femaleapp',include('femaleapp.urls',namespace='femaleapp')),
	path('chat', views.chat, name="chat"),
	path('welcome', views.welcome, name="welcome"),
	path('login', views.login_call,name="login_call"),
    path('logout',views.logout_call,name="logout_call"),
	
]