from django.contrib import admin
from cs.models import Board
from cs.models import Inquire
from cs.models import B_Photo

class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'title',)

admin.site.register(Board, BoardAdmin)

class InquireAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'answer',)

admin.site.register(Inquire, InquireAdmin)

class B_PhotoAdmin(admin.ModelAdmin):
    list_display = ('photo',)

admin.site.register(B_Photo, B_PhotoAdmin)
