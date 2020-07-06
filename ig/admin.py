from django.contrib import admin
from .models import tags,Profile,Post

# Register your models here.
admin.site.register(Profile)
admin.site.register(tags) 
admin.site.register(Post) 