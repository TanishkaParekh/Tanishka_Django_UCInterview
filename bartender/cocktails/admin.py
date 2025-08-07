from django.contrib import admin
from .models import search_cocktail, search_ingredient
# Register your models here.
admin.site.register(search_cocktail)
admin.site.register(search_ingredient)  