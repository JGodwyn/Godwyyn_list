from django.contrib import admin
from .models import Search


class Search_display(admin.ModelAdmin):
    list_display = ('search', 'created')


admin.site.register(Search, Search_display)
