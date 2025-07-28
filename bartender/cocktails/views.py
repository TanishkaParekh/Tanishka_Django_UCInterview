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
    name_data = []
    instruction_list = []
    ingredients = []
    ingredient_drinks = []
    submitted = False
    NoResult = False
                    
    if request.method == 'GET':
        form = search_cocktail(request.GET)
        if form.is_valid():
            submitted = True
            # Get the search term from the form
            search = form.cleaned_data['search']

            #fetch drink by name
            drinkName_url = f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={search}'
            response1 = requests.get(drinkName_url)
            client_data1 = response1.json() #dictionery
            drink_data = client_data1.get('drinks') or []
            

            #fetch drink by ingredient
            ingredientName_url = f'https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={search}'
            response2 = requests.get(ingredientName_url)
            client_data2 = response2.json()
            ingredient_data = client_data2.get('drinks') or []
            
            # If no drinks found, set NoResult to True
            if not drink_data and not ingredient_data:
                NoResult = True
               
            # Process instructions and ingredients for each drink
            for drink in drink_data:
                if 'idDrink' in drink:
                    #extracting ingredients
                    ingredients = []
                    instruction_list = []
                    for i in range(1,4):
                        ingredient = drink.get(f'strIngredient{i}')
                        measure = drink.get(f'strMeasure{i}')
                        if ingredient and ingredient.strip():  # Check if ingredient is not None and not empty
                            ingredients.append({
                                'name': ingredient.strip(),
                                'measure': measure.strip() if measure and measure.strip() else ' '
                            })
                    if drink['strInstructions']:
                        instructions = drink.get('strInstructions',[])                    # Split instructions by period and strip whitespace
                        instruction_list = [sentence.strip() for sentence in instructions.split('.') if sentence.strip()]
                    else:
                        instruction_list= []
                    drink['instruction_list'] = instruction_list
                    drink['ingredients'] = ingredients
                
            ingredient_drinks = []
            for ingredient in ingredient_data:
                if 'idDrink' in ingredient:
                    #extracting ingredients
                    drink_name = ingredient.get('strDrink')
                    drink_details_url = f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink_name}'
                    response = requests.get(drink_details_url)
                    details_data = response.json()
                    name_data = details_data.get('drinks')
                    if name_data is None:
                        name_data = []
                    for drink in name_data:
                        ingredients = []
                        instruction_list = []
                        for i in range(1, 4):
                            ingredient_name = drink.get(f'strIngredient{i}')
                            measure = drink.get(f'strMeasure{i}')
                            if ingredient_name and ingredient_name.strip():
                                ingredients.append({
                                    'name': ingredient_name.strip(),
                                    'measure': measure.strip() if measure and measure.strip() else ' '
                                })
                        if drink['strInstructions']:
                            instructions = drink.get('strInstructions', '')
                            instruction_list = [sentence.strip() for sentence in instructions.split('.') if sentence.strip()]
                        else:
                            instruction_list = []
                        drink['instruction_list'] = instruction_list
                        drink['ingredients'] = ingredients
                        ingredient_drinks.append(drink)
    else:
        form = search_cocktail()
    
    return render(request,'cocktail_search.html',
                  {'form':form , 
                   'drink_data':drink_data , 'ingredients':ingredients,
                   'ingredient_data':ingredient_drinks , 'name_data':name_data , 'instruction_list': instruction_list,
                   'submitted':submitted, 'NoResult':NoResult})


def SearchPage(request):
    drink_data=[]
    ingredient_data=[]  
    submitted = False
    NoResult = False
                    
    if request.method == 'GET':
        form = search_cocktail(request.GET)
        if form.is_valid():
            submitted = True
            # Get the search term from the form
            search = form.cleaned_data['search']

            #fetch drink by name
            drinkName_url = f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={search}'
            response1 = requests.get(drinkName_url)
            client_data1 = response1.json() #dictionery
            drink_data = client_data1.get('drinks') or []
            

            #fetch drink by ingredient
            ingredientName_url = f'https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={search}'
            response2 = requests.get(ingredientName_url)
            client_data2 = response2.json()
            ingredient_data = client_data2.get('drinks') or []
            
            # If no drinks found, set NoResult to True
            if not drink_data and not ingredient_data:
                NoResult = True  
    else:
        form = search_cocktail()
    
    return render(request,'search_page.html',
                  {'form':form , 
                   'drink_data':drink_data , 'ingredient_data':ingredient_data,
                   'submitted':submitted, 'NoResult':NoResult})

def cocktail_details(request,drink_id):
    url_cocktail=f'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={drink_id}'
    response = requests.get(url_cocktail)
    client_data = response.json()

    if not client_data or 'drinks' not in client_data or not client_data['drinks']:
        return HttpResponse("No cocktail found with the provided ID.")
    drink_data = client_data['drinks'][0]
    ingredients = []
    for i in range(1, 4):
        ingredient_name = drink_data.get(f'strIngredient{i}')
        measure = drink_data.get(f'strMeasure{i}')
        if ingredient_name and ingredient_name.strip():
            ingredients.append({
                'name': ingredient_name.strip(),
                'measure': measure.strip() if measure and measure.strip() else ' '
            })
    comtext ={'name':drink_data['strDrink'],
              'alcoholic':drink_data['strAlcoholic'],
              'instructions':drink_data['strInstructions'],
              'ingredients':ingredients,
              'image':drink_data['strDrinkThumb']}
    return render(request,'task3.html',context=comtext)
