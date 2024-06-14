from django.contrib import admin
from .models import User,Book,Club, Comment, ClubMembership, Message,Forum

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Club)
admin.site.register(Comment)
admin.site.register(ClubMembership)
admin.site.register(Message)
admin.site.register(Forum)
