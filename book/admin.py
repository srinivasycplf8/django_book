from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from . models import Book

# Register your models here.



admin.site.register(Book)