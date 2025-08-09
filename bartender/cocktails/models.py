from django.db import models

# Create your models here.
class search_cocktail(models.Model):
    search = models.CharField(max_length=300)
    cocktail_name = models.CharField(max_length=100, unique=True , default="Unknown")
    count_cocktail= models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cocktail_name} ({self.count_cocktail})"

class search_ingredient(models.Model):
    search = models.CharField(max_length=300)
    ingredient_name = models.CharField(max_length=100, unique=True , default="Unknown")
    count_ingredient = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.ingredient_name} ({self.count_ingredient})"

class search_drink(models.Model):
    search = models.CharField(max_length=300)
    drink_name = models.CharField(max_length=100, unique=True , default="Unknown")
    count_drink = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.drink_name} ({self.count_drink})"


