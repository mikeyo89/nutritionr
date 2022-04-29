from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.core.cache import caches

from .models import RecipeIngredientsModel, RecipeNutritionModel, RecipeModel, IngredientsModel

import requests
import json

# Create your views here.
class HomeView(generic.TemplateView):
    """ Landing/Index View of the Site. """
    template_name = 'home.html'

class RecipeResultsView(generic.TemplateView):
    template_name = 'recipe_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_query = self.request.GET.get('recipe_name', '')
        search_recommendation = self.request.GET.get('recommendation', '')

        # TODO: Add script logic.
        # TODO: Add caching logic of results. 

        context.update({"search_query": search_query, "recommendation": search_recommendation})
        return context

class FoodResultsView(generic.TemplateView):
    template_name = 'food_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('food_item', '')

        # Get API response data for specified consumable.
        url = "https://edamam-food-and-grocery-database.p.rapidapi.com/parser"
        querystring = {"ingr": search_query}

        headers = {
            "X-RapidAPI-Host": "edamam-food-and-grocery-database.p.rapidapi.com",
            "X-RapidAPI-Key": "a5b0806962mshe36b0ed1b7175d5p152becjsnc7ea3913781c"
        }
        
        # Caching of search results for smarter use of GET requests.
        cache = caches['default']
        data = cache.get(search_query)

        # If results for this search are NOT cached, make a GET request instead.
        if data is None:
            print(f'Cache miss for search query: {search_query}. Making GET request...')
            response = requests.get(url, headers=headers, params=querystring)
            data = json.loads(response.text)['hints']

            if data is not None:
                cache.set(search_query, data)
            else:
                print('JSON response from API GET returned None.')
        else:
            print(f'Cache hit for search query: {search_query}')

        # Get top 5 results of items for search term 'search_query'
        results: list[IngredientsModel] = []
        for x in range(len(data)):
            raw_nutrients = data[x]['food']['nutrients']
            try:
                result = IngredientsModel(data[x]['food']['foodId'] + f'{x}', data[x]['food']['label'], raw_nutrients['ENERC_KCAL'], raw_nutrients['PROCNT'], raw_nutrients['FAT'], raw_nutrients['FIBTG'], data[x]['food']['image'])
                results.append(result)
            except:
                print(f'Could not add food item from result: {data[x]["food"]}')
        
        context.update({"results": results[:5], "search_query": search_query})
        return context