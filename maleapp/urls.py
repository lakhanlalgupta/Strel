from django.urls import path
from . import views

app_name='maleapp'

urlpatterns = [
	path('', views.home),
	path('/fullprofile/<int:id>',views.fullprofile,name="fullprofile"),
	path('/mnextprocess/<int:id>',views.NextProcess,name="NextProcess"),
	path('/rrtomale',views.rrtomale,name="rrtomale"),
	path('/rejectthisgirl/<int:id>',views.rejectthisgirl,name="rejectthisgirl"),
	path('/acceptthisgirl/<int:id>',views.acceptthisgirl,name="acceptthisgirl"),

	path('/brtofemale/<int:id>',views.brtofemale,name="brtofemale"),
	path('/brtomalelist',views.brtomalelist,name="brtomalelist"),
	path('/brdeclinebymale',views.brdeclinebymale,name="brdeclinebymale"),
	path('/yesbreakup',views.yesBreakUp,name="yesBreakUp"),
	
	path('/superbreakup',views.superbreakup,name="superbreakup"),

	
	
]