from django.contrib import admin
from .models import Follow, LikePost, Profile, Post
# Register your models here.

admin.site.register(Profile)### registra el modelos Profile en el Django Admin administrator
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Follow)