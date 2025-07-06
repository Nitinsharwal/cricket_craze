from django.contrib import admin
from .models import Contact

admin.site.register(Contact)
admin.site.site_header = "Cricket Craze Admin Panel"
admin.site.site_title = "Cricket Craze Admin"
admin.site.index_title = "Welcome to Cricket Craze Dashboard"
