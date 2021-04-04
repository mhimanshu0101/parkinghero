from django.contrib import admin
from accounts.models import *
# Register your models here.

admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('id', 'email')