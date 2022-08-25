from django.contrib import admin
from user.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'contact')

# Register your models here.
admin.site.register(User, UserAdmin)