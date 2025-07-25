from django.db import models

# Create your models here.
class search_cocktail(models.Model):
    search = models.CharField(max_length=300)

