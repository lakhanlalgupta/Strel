from django.urls import path
from django.urls import path
from . import views

app_name='femaleapp'

urlpatterns = [
	path('', views.home),
	path('/fullprofile/<int:id>',views.fullprofile,name="fullprofile"),
	path('/fnextprocess/<int:id>',views.NextProcess,name="NextProcess"),
	
	path('/rrtofemale',views.rrtofemale,name="rrtofemale"),
	path('/rejectthisboy/<int:id>',views.rejectthisboy,name="rejectthisboy"),
	path('/acceptthisboy/<int:id>',views.acceptthisboy,name="acceptthisboy"),

	path('/brtomale/<int:id>',views.brtomale,name="brtomale"),
	path('/brtofemalelist',views.brtofemalelist,name="brtofemalelist"),
	path('/brdeclinebyfemale',views.brdeclinebyfemale,name="brdeclinebyfemale"),
	path('/yesbreakup',views.yesBreakUp,name="yesBreakUp"),

	path('/superbreakup',views.superbreakup,name="superbreakup"),
	
]