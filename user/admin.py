from django.contrib import admin

# Register your models here.
from .models import Profile, RelationshipStatus, Friend_Request, Accepted, BreakUp, NewChatApp
admin.site.register(Profile)
admin.site.register(RelationshipStatus)
admin.site.register(Friend_Request)
admin.site.register(Accepted)
admin.site.register(BreakUp)
admin.site.register(NewChatApp)
