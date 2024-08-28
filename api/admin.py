from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserAPI)
admin.site.register(ApiMethod)
admin.site.register(ApiParams)