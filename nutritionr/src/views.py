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

        # Get the user inputs for the GET request.
        search_query = self.request.GET.get('recipe_name', '')
        search_diet = self.request.GET.get('diet', '')

        # Setup the GET request.
        url = "https://edamam-recipe-search.p.rapidapi.com/search"
        params = {"q": search_query, "r": search_diet} if not search_diet or search_diet != '' else {"q": search_query}

        headers = {
            "X-RapidAPI-Host": "edamam-recipe-search.p.rapidapi.com",
            "X-RapidAPI-Key": "a5b0806962mshe36b0ed1b7175d5p152becjsnc7ea3913781c"
        }

        # Caching of search results for smarter use of GET requests.
        query = f'?recipe_name={search_query}&diet={search_diet}'
        cache = caches['default']
        data = cache.get(query)

        # If results for this search are NOT cached, make a GET request instead.
        if data is None:
            print(f'Cache miss for search query: {query}. Making GET request...')
            response = requests.get(url, headers=headers, params=params)
            data = json.loads(response.text)

            if data is not None:
                cache.set(query, data)
            else:
                print('JSON response from API GET returned None.')
        else:
            print(f'Cache hit for search query: {search_query}')

        # Lets iterate through the Top 5 Recipe results and gather data for each Recipe returned.
        results: list[RecipeModel] = []
        for index in range(len(data["hits"])):
            raw_results = data["hits"][index]["recipe"]
            ingredients = [RecipeIngredientsModel(ingredient["text"], ingredient["image"]) for ingredient in raw_results["ingredients"]]
            total_nutrition = RecipeNutritionModel(raw_results["totalNutrients"], 1)
            serving_nutrition = RecipeNutritionModel(raw_results["totalNutrients"], float(raw_results["yield"]))
            total_daily = RecipeNutritionModel(raw_results["totalDaily"], 1)
            serving_daily = RecipeNutritionModel(raw_results["totalDaily"], float(raw_results["yield"]))

            results.append(RecipeModel(f"recipe{index}", raw_results["label"], raw_results["cuisineType"], raw_results["shareAs"], raw_results["yield"], ingredients, total_nutrition, serving_nutrition, total_daily, serving_daily))

        context.update({"search_query": search_query, "diet": search_diet, "results": results[:5]})
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
                cache.set(f'?food_item={search_query}', data)
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
                print(f'Could not add food item from result: {data[x]["food"]["label"]}')
        
        context.update({"results": results[:5], "search_query": search_query})
        return context