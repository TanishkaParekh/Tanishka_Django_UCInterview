from django.contrib import admin
from .models import search_cocktail, search_ingredient,search_drink
# Register your models here.
admin.site.register(search_cocktail)
admin.site.register(search_ingredient)  
admin.site.register(search_drink)