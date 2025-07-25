from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
import json
import requests
# Create your views here.

def home(request):
    return render(request,'home.html')
def SearchCocktail(request):
    drink_data=[]
    ingredient_data=[]
    if request.method == 'GET':
        form = search_cocktail(request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']

            drinkName_url = f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={search}'
            response1 = requests.get(drinkName_url)
            client_data1 = response1.json() #dictionery
            drink_data = client_data1.get('drinks',[])

            ingredientName_url = f'https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={search}'
            response2 = requests.get(ingredientName_url)
            client_data2 = response2.json()
            ingredient_data = client_data2.get('drinks',[])

            for drink in drink_data:
                if drink['strInstructions']:
                    instructions = drink.get('strInstructions','')                    # Split instructions by period and strip whitespace
                    drink['instructions_list'] = [sentence.strip() for sentence in instructions.split('.') if sentence.strip()]
                else:
                    drink['instructions_list'] = []
    else:
        form = search_cocktail()
    
    return render(request,'cocktail_search.html',{'form':form , 'drink_data':drink_data , 'ingredient_data':ingredient_data})