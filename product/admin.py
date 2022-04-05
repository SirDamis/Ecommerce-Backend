from gzip import READ
from django.contrib import admin

from .models import Reviews, Products

admin.site.register(Reviews)
admin.site.register(Products)