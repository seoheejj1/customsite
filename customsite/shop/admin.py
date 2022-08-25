from django.contrib import admin
from shop.models import Config, Co_account

class ConfigAdmin(admin.ModelAdmin):
    list_diplay = ('name', 'ceo')

class Co_accountAdmin(admin.ModelAdmin):
    list_display = ('bank', 'number', 'depositer')

admin.site.register(Config, ConfigAdmin)
admin.site.register(Co_account, Co_accountAdmin)

