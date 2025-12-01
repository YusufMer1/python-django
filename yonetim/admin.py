from django.contrib import admin
from .models import Sakin, Daire, Aidat

# Modellerimizi Admin paneline kaydetme
admin.site.register(Sakin)
admin.site.register(Daire)
admin.site.register(Aidat)


