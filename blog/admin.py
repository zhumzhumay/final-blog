from django.contrib import admin

from .models import User, Post, Comment, Advertising

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Advertising)
admin.site.register(Comment)
# Register your models here.
