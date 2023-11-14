from django.contrib import admin
from django.conf.locale.pt_BR import formats as portuguese
from django.conf.locale.en import formats as english
from .models import Chat

portuguese.DATE_FORMAT = 'd/m/Y'
english.DATE_FORMAT = 'd/m/Y'

@admin.register(Chat)
class ChatRegister(admin.ModelAdmin):
    list_display = ['id', 'user']
    list_display_links = ['id', 'user']
    list_per_page = 25
    search_fields = ['user']
    ordering = ['user']
