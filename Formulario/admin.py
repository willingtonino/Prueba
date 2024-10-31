from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Section, Form, Company

admin.site.register(Section)
admin.site.register(Form)
admin.site.register(Company)