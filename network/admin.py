from django.contrib import admin
from .models import User,Blogpost,Followinfo,Like
# Register your models here.
admin.site.register(User)
admin.site.register(Blogpost)
admin.site.register(Followinfo)
admin.site.register(Like)